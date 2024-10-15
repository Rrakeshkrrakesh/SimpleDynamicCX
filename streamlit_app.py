import streamlit as st
import pandas as pd

# Define the configuration matrix
matrix = {
    'Energy Flow': {'Default': 'pass', 'Solar $': 'include', 'Solar kWh': 'include', 'EV': 'pass', 'AMI': 'pass'},
    'Cumulative Balance': {'Default': 'pass', 'Budget Billing $': 'include', 'Budget Billing kWh': 'include'},
    'TOU Usage & Cost': {'Default': 'pass', 'TOU Rate': 'include', 'Solar $': 'kill', 'Solar kWh': 'kill'},
    'Solar Production': {'Default': 'pass', 'Solar $': 'include', 'Solar kWh': 'include'}
}

dimensions = ['TOU Rate', 'Solar $', 'Solar kWh', 'EV', 'Budget Billing $', 'Budget Billing kWh', 'AMI']
elements = list(matrix.keys())

# Define color mapping for dimensions
dimension_colors = {
    'TOU Rate': 'lightblue',
    'Solar $': 'lightyellow',
    'Solar kWh': 'gold',
    'EV': 'lightgreen',
    'Budget Billing $': 'lightcoral',
    'Budget Billing kWh': 'salmon',
    'AMI': 'lightgray'
}

st.set_page_config(layout="wide")
st.title("Dynamic CX Configuration Matrix")

# Sidebar for dimension selection
st.sidebar.header("Select User Dimensions")
selected_dimensions = st.sidebar.multiselect("Choose dimensions:", dimensions)

# Explanation
# ... (Explanation logic remains the same)

# Generate table data with color coding
table_data = []
for element in elements:
    row_data = {'Element': element}
    status = 'pass'
    reason = 'Default pass'
    for dim in dimensions:
        if dim in matrix[element]:
            cell_value = matrix[element][dim]
            if cell_value == 'kill':
                status = 'kill'
                reason = f'{dim} dimension kills this element'
                row_data[dim] = f'Kill ({reason})'  # Add reason to cell
            elif cell_value == 'include' and status != 'kill':
                status = 'include'
                reason = f'{dim} dimension includes this element'
                row_data[dim] = f'Include ({reason})'  # Add reason to cell
            else:
                row_data[dim] = cell_value
        else:
            row_data[dim] = '-'  # Mark dimensions not in matrix as '-'

    row_data['Status'] = 'Included' if status == 'include' else 'Not Included'
    row_data['Reason'] = reason
    table_data.append(row_data)

# Display table with color coding
df = pd.DataFrame(table_data)

# Styling function for color-coding
def highlight_cells(val):
    """Highlights cells based on dimension and action."""
    for dim, color in dimension_colors.items():
        if dim in str(val):  # Check if dimension is in the cell value
            if 'Kill' in str(val):
                return f'background-color: {color}; color: red'
            elif 'Include' in str(val):
                return f'background-color: {color}; color: green' 
    return '' 

st.dataframe(df.style.applymap(highlight_cells))

# ... (Rest of the code: "How it works", raw matrix display) 
