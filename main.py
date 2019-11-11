import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt

plt.figure(figsize=(40, 40))
G = nx.Graph()


def main():
    df = pd.read_excel(r'./Supplier_Assurance.xlsx', index_col=0, usecols="A:C,F")
    df['Domain'] = df['Domain'].fillna(method='ffill')
    abc = (df.groupby(['Domain'])
           .apply(lambda x: dict(zip(x.Question, x.Score)))
           .reset_index()
           .rename(columns={0: 'Question_Scores'})
           .to_json(orient='records'))
    js_graph = json.loads(abc)
    for js in js_graph:
        G.add_edge('Risk Score', js['Domain'])
        for key, value in js["Question_Scores"].items():
            G.add_edge(js['Domain'], key)
    pos_random = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos_random, node_size=30, node_color="red", node_shape='s', alpha=1)
    nx.draw_networkx_edges(G, pos_random, alpha=0.5)
    nx.draw_networkx_labels(G, pos_random, alpha=1, font_size=5)
    plt.axis('off')
    plt.title('Supplier Assurance Risk Map')
    plt.savefig('plot.png')
    plt.show()


if __name__ == '__main__':
    main()
