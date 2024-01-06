import TabClasses as T

class Registry:
    _instance = None
    instances = {}
    directory = "C:/Users/Michelle/Documents/Obsidian Notes/StargateTTRPG/GameObjects"
    def __new__(cls):
       if not cls._instance:
           cls._instance = super(Registry, cls).__new__(cls)
       Registry.load_instances(Registry.directory)
    
    def add_instance(instance):
        instance_class = instance.type
        if instance_class not in Registry.instances:
            Registry.instances[instance_class] = {}
        if instance_class == "Aliens":
            instance_race = instance.race
            if instance_race not in Registry.instances[instance_class]:
                Registry.instances[instance_class][instance_race] = []
            Registry.instances[instance_class][instance_race].append(instance)
        elif instance_class == 'Planets':  # Changed 'if' to 'elif' here
            if instance.name not in Registry.instances[instance_class]:
                Registry.instances[instance_class][instance.name] = []
            Registry.instances[instance_class][instance.name].append(instance)

    def save_instances(directory):
        for instance_class, instances in Registry.instances.items():
            class_directory = T.os.path.join(directory, instance_class)
            T.os.makedirs(class_directory, exist_ok=True)
            for sub_instance_class, sub_instances in instances.items():
                sub_class_directory = T.os.path.join(class_directory, sub_instance_class)
                T.os.makedirs(sub_class_directory, exist_ok=True)
                for instance in sub_instances:
                    filename = T.os.path.join(sub_class_directory, f'{instance.name}.md')
                    front_matter = {attr: value for attr, value in instance.__dict__.items() if attr != 'name'}
                    # Read the existing content
                    with open(filename, 'r') as file:
                        content = file.read()
                        match = T.re.search(r'---\n(.*?)\n---', content, T.re.DOTALL)
                        if match:
                            # Update the front matter
                            content = content.replace(match.group(0), f'---\n{T.yaml.dump(front_matter)}---\n')
                        else:
                            # Add the front matter if it doesn't exist
                            content = f'---\n{T.yaml.dump(front_matter)}---\n{content}'
                    # Write the updated content back to the file
                    with open(filename, 'w') as file:
                        file.write(content)
        # Registry.instances = instances

    def load_instances(directory):
        Registry.instances = {'Aliens':{}, 'Planets':{}}
        T.CoreRulebookValues.PLANETS = []
        T.CoreRulebookValues.ALIEN_TYPES = []
        for i, (root, dirs, files) in enumerate(T.os.walk(directory)):
            # if root == os.path.join(directory, '*'):
            if root == T.os.path.join(directory, 'Aliens'):
                T.CoreRulebookValues.ALIEN_TYPES = dirs
                for alien in dirs:
                    if alien not in Registry.instances['Aliens']:
                        Registry.instances['Aliens'][alien]= []

            if root == os.path.join(directory, 'Planets'):
                T.CoreRulebookValues.PLANETS = dirs
                for planet in dirs:
                    if planet not in Registry.instances['Planets']:
                        Registry.instances['Planets'][planet]= []

                variable_value = os.path.basename(root)

            if root == T.os.path.join(directory, 'Aliens', '*'):
                variable_value = T.os.path.basename(root)
                for file in files:
                    with open(T.os.path.join(root, file), 'r') as f:
                        content = f.read()
                        match = T.re.search(r'---\n(.*?)\n---', content, T.re.DOTALL)
                        if match:
                            # Load the front matter
                            front_matter = T.yaml.load(match.group(1), Loader=T.yaml.FullLoader)
                            # Create an instance of the class
                            instance_class_obj = globals()[T.NPC()]
                            instance = instance_class_obj(**front_matter)
                            Registry.instances['Aliens'][variable_value].append(instance)
                        else:
                            instance_class_obj = globals()[NPC()]
                            instance = instance_class_obj()
                            Registry.instances['Aliens'][variable_value].append(instance)
            
            if root == T.os.path.join(directory, 'Planets', '*'):
                variable_value = T.os.path.basename(root)
                for file in files:
                    with open(T.os.path.join(root, file), 'r') as f:
                        content = f.read()
                        match = T.re.search(r'---\n(.*?)\n---', content, T.re.DOTALL)
                        if match:
                            # Load the front matter
                            front_matter = T.yaml.load(match.group(1), Loader=T.yaml.FullLoader)
                            # Create an instance of the class
                            instance_class_obj = globals()[T.NPC()]
                            instance = instance_class_obj(**front_matter)
                            Registry.instances['Aliens'][variable_value].append(instance)
                        else:
                            instance_class_obj = globals()[T.NPC()]
                            instance = instance_class_obj()
                            Registry.instances['Aliens'][variable_value].append(instance)