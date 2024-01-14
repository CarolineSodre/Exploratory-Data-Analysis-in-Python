import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt


# Loading the dataset #

data = pd.read_csv('C:/Users/carol/Analise_de_dados_py/DSA/Projeto_2/dataset.csv')

# Head of the dataset
print(data.head())

# Columns of the dataset
#print(data.columns)

# Checking for null values
#print(data.isnull().sum())


# Analysing the dataset and answering some questions about it #

print(data['Valor_Venda'].describe())


# 1. Which City has the Highest Sales Value for Products in the 'Office Supplies' Category?

# Taking only the products in the 'Office Supplies' category
data_off_supp_by_cat = data[data['Categoria'] == 'Office Supplies']

# Grouping by the city and summing the Sales Value, then asking for the index of the highest value
city_id = data_off_supp_by_cat.groupby('Cidade')['Valor_Venda'].sum().idxmax()

print("The city with the highest sales value for 'Office Supplies' is", city_id)


# 2. What is the Total Sales by Order Date? Demonstrate the result through a graph.

# Grouping 'Data_Pedido' and 'Valor_Venda' and using the sum function to get the Total Sales by Order Date
data_order_date_by_sales_sum = data.groupby('Data_Pedido')['Valor_Venda'].sum()
print(data_order_date_by_sales_sum)

# Creating a bar graph 
plt.figure(figsize = (10, 5))
data_order_date_by_sales_sum.plot(color = 'black')
plt.xlabel('Order Date')
plt.ylabel('Total Sales')
plt.title('Total Sales by Order Date')
plt.show()  


# 3. What is the Total Sales by State? Demonstrate the result through a bar graph.

data_sales_by_state_sum = data.groupby('Estado')['Valor_Venda'].sum()

print(data_sales_by_state_sum.head())

# Creating a bar graph 
plt.figure(figsize = (10, 5))
data_sales_by_state_sum.plot.bar(color = 'black')   
plt.title('Total Sales by State')
plt.xlabel('State')
plt.ylabel('Total Sales')
plt.show()


# 4 What are the 10 Cities with the Highest Total Sales? Demonstrate the result through a bar graph.

cities_hts = data_sales_by_state_sum.sort_values(ascending = False)
print("The 10 Cities with the Highest Total Sales are: \n", cities_hts.head(10))

# Creating a bar graph 
plt.figure(figsize = (10, 5))
cities_hts.plot.bar(color = 'black')   
plt.title('The 10 Cities with the Highest Total Sales')
plt.xlabel('City')
plt.ylabel('Total Sales')
plt.show()


# 5. Which Segment Had the Highest Total Sales? Show the result using a pie chart.

data_sales_by_segment_sum = data.groupby('Segmento')['Valor_Venda'].sum()

autopct_pie_plot = (data_sales_by_segment_sum[0], data_sales_by_segment_sum[1], data_sales_by_segment_sum[2])

print("The Segment that Had the Highest Total Sales was: ", data_sales_by_segment_sum.idxmax())

# Creating a pie graph 
plt.figure(figsize = (10, 10))
data_sales_by_segment_sum.plot.pie(colors = {'lightblue', 'lightcoral', 'lightgreen'}, autopct = lambda p: '{:.2f}%  ({:,.0f})'.format(p, p*sum(data_sales_by_segment_sum)/100))

# Clean the central circle
centre_circle = plt.Circle((0, 0), 0.82, fc = 'white')
plt.gcf().gca().add_artist(centre_circle)
plt.ylabel('')
plt.title('Total Sales by Segment')
plt.show()


# 6. What is the Total Sales Per Segment and Per Year?

# Use the 'Data_Pedido colum to split the year
data['Year'] = data['Data_Pedido'].str.split('/').str[2] 
# Or convert the date column to datetime type to get the proper format, then extract the year by creating a new variable
#data['Data_Pedido'] = pd.to_datetime(data['Data_Pedido'], dayfirst = True)
#data['Year'] = data['Data_Pedido'].dt.year

data_sales_by_segment_and_yr_sum = data.groupby(['Year', 'Segmento'])['Valor_Venda'].sum()
print(data_sales_by_segment_and_yr_sum)


# 7. The company's managers are considering granting different ranges of discounts and would like to carry out a simulation based on the rule below:
#If the Sales_Value is greater than 1000, you receive a 15% discount.
#If the Sales_Value is less than 1000, you receive a 10% discount.

def calculate_discount(sales_value):
    if sales_value > 1000:
        return 0.15  # 15% discount
    else:
        return 0.10  # 10% discount

# Apply discounts to each sale
for i, sale in enumerate(data['Valor_Venda']):
    valor_venda = sale
    discount_rate = calculate_discount(valor_venda)
    data.at[i,'Discount_Rate'] = discount_rate
    data.at[i,'Discounted_Value'] = valor_venda * (1 - discount_rate)
    
print(data['Discount_Rate'].value_counts())


# 8. Consider That the Company Decides to Grant a 15% Discount on the Previous Item. What would be the average sales value before and after the discount?

print("Average sales value before the discount:", data.loc[data['Discount_Rate'] == 0.15, 'Valor_Venda'].mean())
print("Average sales value after the discount:", data.loc[data['Discount_Rate'] == 0.15, 'Discounted_Value'].mean())


# 9. What is the Average Sales Per Segment, Per Year and Per Month? Demonstrate the result through a line graph.

data['Month'] = data['Data_Pedido'].str.split('/').str[1]
mean_by_yr_by_month_by_seg = data.groupby(['Year', 'Month', 'Segmento'])['Valor_Venda'].mean().reset_index()

# Plotting the data for each year
for year in mean_by_yr_by_month_by_seg['Year'].unique():
    plt.figure(figsize=(10, 6))
    
    # Filter data for the specific year
    year_data = mean_by_yr_by_month_by_seg[mean_by_yr_by_month_by_seg['Year'] == year]
    
    # Plotting for each segment
    for segment in year_data['Segmento'].unique():
        segment_data = year_data[year_data['Segmento'] == segment]
        plt.plot(segment_data['Month'], segment_data['Valor_Venda'], label=segment)
    
    plt.title(f'Mean Sales by Month for {year}')
    plt.xlabel('Month')
    plt.ylabel('Mean Sales')
    plt.legend()
    plt.show()


# 10. What is the Total Sales Per Category and SubCategory, Considering Only the Top 12 SubCategories? Show everything through a single graph.

total_sales_per_subcategory = data.groupby(['Categoria', 'SubCategoria'])['Valor_Venda'].sum().reset_index()

# Sort the subcategories within each category based on total sales
total_sales_per_subcategory['Rank'] = total_sales_per_subcategory.groupby('Categoria')['Valor_Venda'].rank(ascending=False, method='dense')
total_sales_per_subcategory = total_sales_per_subcategory[total_sales_per_subcategory['Rank'] <= 12]

# Display or further analyze the result
print(total_sales_per_subcategory)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

# Use pivot_table to organize data for stacked bar chart
pivot_table = total_sales_per_subcategory.pivot_table(index='Categoria', columns='SubCategoria', values='Valor_Venda', fill_value=0)

pivot_table.plot(kind='bar', stacked=True, ax=ax)

plt.title('Total Sales Per Category and Top 12 SubCategories')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.legend(title='SubCategory', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()



















