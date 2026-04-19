from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

import os

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = os.getenv("groq_api_key")
)

prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest only the a fancy name for this,give only one name dont need explanation."
    )


prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="""Suggest some menu items for {restaurant_name}. Return it as a comma separated string"""
    )

def generate_restaurant_name_and_items(cuisine):
    # Chain 1: Restaurant Name
    

    name_chain = prompt_template_name | llm
    name = name_chain.invoke({"cuisine":cuisine})
    restaurant_name = name.content.strip() 

    # Chain 2: Menu Items
    menu_chain = prompt_template_items | llm
    menu = menu_chain.invoke({"restaurant_name":restaurant_name})
    menu_item = menu.content.strip()


    return {
            "restaurant_name":restaurant_name,
            "menu_items":menu_item
            }

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Italian"))
