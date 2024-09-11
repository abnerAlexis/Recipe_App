from io import BytesIO 
import base64
import matplotlib.pyplot as plt
import pandas as pd



def get_graph():
   #create a BytesIO buffer for the image
   buffer = BytesIO()         

   #create a plot with a bytesIO object as a file-like object. Set format to png
   plt.savefig(buffer, format='png')

   #set cursor to the beginning of the stream
   buffer.seek(0)

   #retrieve the content of the file
   image_png=buffer.getvalue()

   #encode the bytes-like object
   graph=base64.b64encode(image_png)

   #decode to get the string as output
   graph=graph.decode('utf-8')

   #free up the memory of buffer
   buffer.close()

   #return the image/graph
   return graph


def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(6, 3))

    # Split ingredients into individual items
    data['ingredients'] = data['ingredients'].apply(lambda x: x.split(','))

    # Flatten the list of ingredients
    all_ingredients = [ingredient.strip() for sublist in data['ingredients'] for ingredient in sublist]

    # Count occurrences of each ingredient
    ingredient_counts = pd.Series(all_ingredients).value_counts()

    if chart_type == '#1':
        plt.figure(figsize=(8, 6))  # Width: 8 inches, Height: 6 inches

        # Bar chart: Count occurrences of each ingredient
        plt.bar(ingredient_counts.index, ingredient_counts.values)

        # Rotate the x-axis labels by 50 degrees and align to the right
        plt.xticks(rotation=50, ha='right')

        plt.xlabel('Ingredients')  # Add x-axis label
        plt.ylabel('Count')        # Add y-axis label
        plt.title('Ingredient Counts')  # Add a title
        plt.tight_layout()         # Adjust layout to fit everything nicely

        plt.show()  # Display the plot

    elif chart_type == '#2':
        # Pie chart: Proportion of each ingredient in the recipes
        plt.figure(figsize=(10, 10))  # Make the figure a square for the pie chart

        # Create an explode list to separate specific slices
        explode = [0.03] * len(ingredient_counts)

        # Pie chart: Proportion of each ingredient in the recipes
        wedges, texts, autotexts = plt.pie(
            ingredient_counts.values,
            labels=ingredient_counts.index,
            autopct='%1.1f%%',
            startangle=90,  # Start the pie chart from a specific angle
            pctdistance=0.85,  # Distance of percentage labels from the center
            explode=explode,  # Use the explode parameter to separate slices
            textprops=dict(color="black", fontsize=8)  # Change text color to black and set font size
        )

        # Adjust font size for percentage labels
        for autotext in autotexts:
            autotext.set_fontsize(8) 

        plt.title('Proportion of Ingredients in Recipes')  #  : Add a title
        plt.tight_layout()  # Adjust layout to fit everything nicely

        plt.show()  # Display the plot

    elif chart_type == '#3':
        plt.figure(figsize=(8, 6))  # Width: 8 inches, Height: 6 inches

        # Line chart: Ingredient occurrences
        plt.plot(ingredient_counts.index, ingredient_counts.values, marker='o')  # Add markers for data points

        # Rotate the x-axis labels by 50 degrees and align to the right
        plt.xticks(rotation=50, ha='right') 

        plt.xlabel('Ingredients')  # Add x-axis label
        plt.ylabel('Count')        # Add y-axis label
        plt.title('Ingredient Occurrences')  # Add a title
        plt.tight_layout()         # Adjust layout to fit everything nicely

        plt.grid()  # Add grid lines for better readability
        plt.show()  # Display the plot
    else:
        print('Unknown chart type')

    plt.tight_layout()
    chart = get_graph()
    return chart