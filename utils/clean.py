import json

# Carregar o JSON do arquivo config.json
with open('config.json', 'r') as file:
    data = json.load(file)

# Remover as chaves indesejadas
for core in data['cores'].values():
    core.pop('modules', None)
    core.pop('module_graph', None)
    core.pop('module_graph_inverse', None)
    core.pop('non_tb_files', None)

# Salvar o resultado em config2.json
with open('config2.json', 'w') as file:
    json.dump(data, file, indent=4)

print("As chaves indesejadas foram removidas e o novo arquivo foi salvo como config2.json.")
