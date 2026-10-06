import os

from google import genai
from google.genai import types

from tools import AVAILABLE_TOOLS

#create Gemini Client
client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

#Tell Gemini what tools are available
weather_function=types.FunctionDeclaration(
    name="get_weather",
    description="Get the current weather information for a city",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "city":types.Schema(
                type=types.Type.STRING,
                description="The name of the city."
            )
        },
        required=["city"]
    )
)

#Put our function declaration inside a Tool
weather_tool=types.Tool(
    function_declarations=[
        weather_function
    ]
)

def ask_llm(user_message):

    #Start the conversation
    contents=[
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        )
    ]
    #First request to Gemini
    response=client.models.generate_content(
        model="gemin-3.5-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[weather_tool]
        )
    )

    #check whether Gemini requested a tool
    if not response.function_calls:
        return response.text

    #Gemini requested one or more tools
    for function_call in response.function_calls:

        tool_name=function_call.name
        arguments=function_call.args

        print("LLM requested tool:",tool_name)
        print("Arguments:",arguments)

        #find the actual Python function
        tool_function=AVAILABLE_TOOLS.get(tool_name)

        if tool_function is None:
            return f"Unknown tool:{tool_name}"
         # Execute the Python function
        tool_result = tool_function(**arguments)
        print("Tool result:",tool_result)

        #Add Gemini response to conversation
        contents.append(response.candidates[0].content)

        # Add the tool result
        contents.append(
            types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=tool_name,
                        response=tool_result
                    )
                ]
            )
        )

        # Send the tool result back to Gemini
    final_response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[weather_tool]
        )
    )

    return final_response.text