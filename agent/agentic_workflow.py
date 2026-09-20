from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessageState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
# from tools.weather_info_tool import WeatherInfoTool
# from tools.place_search_tool import PlaceSearchTool
# from tools.expense_calculator_tool import CalculatorTool
# from tools.currency_converter_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self):
        self.tools = [
            # WeatherInfoTool(),
            # PlaceSearchTool(),
            # CalculatorTool(),
            # CurrencyConverterTool()
        ]
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessageState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}

# one LLM and multiple tools
# in langraph node=function (agent_function=Brain of my system=functionality=prompt=instruction only)
    def build_graph(self):
        graph_builder=StateGraph(MessageState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition) # agent is passing the cursor to tools_condition and its trying to check whether I need to call the tool or stop the process
        graph_builder.add_edge("tools", "agent") # means it is workingin a loop, back and forth unless we get our final answer, once LLM satisfy then Final response this system is call ReAct system i.e reasoning and action
        # Reasoning=LLM Action=Tool calling
        # multi-agent host these tools as separate-separate agents
        # input and out flowing in the form of state
        # state is list of messages, key message

        graph_builder.add_edge("agent", END)

        self.graph=graph_builder.compile()
        return self.graph


    def __call__(self):
        pass