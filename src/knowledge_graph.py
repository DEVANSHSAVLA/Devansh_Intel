import pandas as pd
import plotly.graph_objects as go
import ast
import os
import numpy as np

def build_knowledge_graph(data_path='data/jobs_cleaned_with_skills.csv'):
    """
    Native DEVANSH Relational Engine: No external graph library required.
    Uses pure-Python adjacency matrices for 100% reliability.
    """
    if not os.path.exists(data_path):
        return go.Figure().add_annotation(text="DATA SOURCE OFFLINE", showarrow=False)
    
    try:
        df = pd.read_csv(data_path)
        df['Extracted Skills'] = df['Extracted Skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        
        # Nodes: Roles and Top Skills
        roles = df['Job Title'].unique().tolist()
        all_skills = [s for sk in df['Extracted Skills'] for s in sk]
        top_skills = pd.Series(all_skills).value_counts().head(20).index.tolist()
        
        nodes = []
        node_map = {} # label -> id
        
        # Add Role Nodes
        for i, r in enumerate(roles):
            nodes.append({'label': r, 'type': 'role', 'color': '#00f2ff', 'size': 15})
            node_map[r] = len(nodes) - 1
            
        # Add Skill Nodes
        for i, s in enumerate(top_skills):
            nodes.append({'label': s, 'type': 'skill', 'color': '#14d1ff', 'size': 10})
            node_map[s] = len(nodes) - 1
            
        # Edges
        edge_x = []
        edge_y = []
        
        # Calculate Coordinates (Simple Circle/Force-ish layout)
        import math
        for i, node in enumerate(nodes):
            angle = (2 * math.pi * i) / len(nodes)
            node['x'] = math.cos(angle)
            node['y'] = math.sin(angle)
            
        for r in roles:
            role_jobs = df[df['Job Title'] == r]
            role_skills = [s for sk in role_jobs['Extracted Skills'] for s in sk if s in top_skills]
            skill_counts = pd.Series(role_skills).value_counts()
            
            for s, count in skill_counts.items():
                if count > 2: # High-signal threshold
                    u = node_map[r]
                    v = node_map[s]
                    edge_x.extend([nodes[u]['x'], nodes[v]['x'], None])
                    edge_y.extend([nodes[u]['y'], nodes[v]['y'], None])
                    
        # Visualize with Plotly
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#3a494b'),
            hoverinfo='none',
            mode='lines'
        ))
        
        fig.add_trace(go.Scatter(
            x=[n['x'] for n in nodes],
            y=[n['y'] for n in nodes],
            mode='markers+text',
            text=[n['label'] if n['type']=='role' else '' for n in nodes],
            textposition="top center",
            marker=dict(
                size=[n['size'] for n in nodes],
                color=[n['color'] for n in nodes],
                line_width=2
            ),
            hovertext=[n['label'] for n in nodes]
        ))
        
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#e1fdff",
            height=600
        )
        return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"RELATIONAL ENGINE ERROR: {str(e)}", showarrow=False, font_size=14, font_color="#ff4b4b")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig
