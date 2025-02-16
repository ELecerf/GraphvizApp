import streamlit as st
import graphviz
import pandas as pd
import io

def generate_graphviz_code(table_input, layout):
    # Set the graph direction based on the selected layout (TB: Top-to-Bottom, LR: Left-to-Right)
    graphviz_code = f"digraph G {{\n  rankdir={layout};\n"
    
    for index, row in table_input.iterrows():
        content = row['ID']
        description = row['Description']
        predecessors = row['Predecessor ID']
        # Use 'ellipse' if Format is specified as ellipse, otherwise default to 'box'
        shape = 'ellipse' if row['Format'].strip().lower() == 'ellipse' else 'box'
        
        # Add node with label and shape
        graphviz_code += f'  {content} [label="{description}", shape={shape}];\n'
        
        # If there are predecessor IDs, create edges
        if predecessors:
            for predecessor in predecessors.split():
                graphviz_code += f'  {predecessor} -> {content};\n'
    
    graphviz_code += "}"
    return graphviz_code

def main():
    st.title("Graphviz Graph Generator")
    
    # Editable dataframe for table input
    table_input = st.data_editor(
        pd.DataFrame(columns=['ID', 'Description', 'Predecessor ID', 'Format']),
        num_rows="dynamic",
        key="table_input"
    )
    
    layout = st.selectbox("Layout (TB or LR):", ["TB", "LR"])
    
    if st.button("Generate Graph"):
        if not table_input.empty:
            graphviz_code = generate_graphviz_code(table_input, layout)
            graph = graphviz.Source(graphviz_code)
            
            # Render the graph as PNG bytes
            try:
                png_data = graph.pipe(format='png')
            except Exception as e:
                st.error(f"An error occurred while generating the PNG: {e}")
                return
            
            # Display the graph image
            st.image(png_data, use_column_width=True)
        else:
            st.warning("Please enter data in the table.")

if __name__ == "__main__":
    main()
