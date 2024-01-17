import os
import TabClasses as T

class Registry:
    _instance = None
    instances = {}
    directory = "C:/Users/Michelle/Documents/Obsidian Notes/StargateTTRPG/GameObjects"
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Registry, cls).__new__(cls)
        cls._instance.load_instances()
        return cls._instance
    
    def add_instance(cls, instance):
        instance_class = instance.type
        if instance_class not in cls._instance.instances:
            cls._instance.instances[instance_class] = {}
        if instance_class == "Aliens":
            instance_race = instance.race
            if instance_race not in cls._instance.instances[instance_class]:
                cls._instance.instances[instance_class][instance_race] = []
            cls._instance.instances[instance_class][instance_race].append(instance)
        else:
            if instance.name not in cls._instance.instances[instance_class]:
                cls._instance.instances[instance_class][instance.name] = []
            cls._instance.instances[instance_class][instance.name].append(instance)

    def save_instances(cls):
        for instance_class, second in cls._instance.instances.items():
            print(instance_class)
            class_directory = T.os.path.join(cls._instance.directory, instance_class)
            T.os.makedirs(class_directory, exist_ok=True)
            for sub_instance_class, sub_instances in cls._instance.instances.items():
                sub_class_directory = T.os.path.join(class_directory, sub_instance_class)
                T.os.makedirs(sub_class_directory, exist_ok=True)
                for instance in sub_instances:
                    #having problem with the following line, saying instance is a string not an object?
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

    def load_instances(cls):
        Registry.instances = {'Aliens':{}, 'Planets':{}}
        T.CoreRulebookValues.PLANETS = []
        T.CoreRulebookValues.ALIEN_TYPES = []
        for i, (root, dirs, files) in enumerate(T.os.walk(cls._instance.directory)):
            # if root == os.path.join(directory, '*'):
            if root == T.os.path.join(cls._instance.directory, 'Aliens'):
                T.CoreRulebookValues.ALIEN_TYPES = dirs
                for alien in dirs:
                    if alien not in Registry.instances['Aliens']:
                        Registry.instances['Aliens'][alien]= []

            if root == os.path.join(cls._instance.directory, 'Planets'):
                T.CoreRulebookValues.PLANETS = dirs
                for planet in dirs:
                    if planet not in Registry.instances['Planets']:
                        Registry.instances['Planets'][planet]= []

                variable_value = os.path.basename(root)

            if root == T.os.path.join(cls._instance.directory, 'Aliens', '*'):
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
            
            if root == T.os.path.join(cls._instance.directory, 'Planets', '*'):
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