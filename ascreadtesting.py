def parse_ltspice_asc(file_path):
    components = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('SYMBOL'):
                component = {}
                parts = line.split()
                component['type'] = parts[1]
                component['x'] = int(parts[2])
                component['y'] = int(parts[3])
                components.append(component)
            elif line.startswith('SYMATTR InstName'):
                component['name'] = line.split()[-1]
            elif line.startswith('SYMATTR Value'):
                component['value'] = line.split()[-1]
    return components

components = parse_ltspice_asc('utilities/draft.asc')
for comp in components:
    print(comp)