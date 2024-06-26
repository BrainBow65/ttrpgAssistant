import os
import json
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
    
    @classmethod
    def add_instance(cls, instance):
        instance_class = instance.type
        if instance_class not in cls.instances:
            cls.instances[instance_class] = {}
        if instance_class == "Aliens":
            instance_race = instance.race
            if instance_race not in cls.instances[instance_class]:
                cls.instances[instance_class][instance_race] = []
            cls.instances[instance_class][instance_race].append(instance)
        else:
            if instance.name not in cls.instances[instance_class]:
                cls.instances[instance_class][instance.name] = []
            # Append the instance to the existing list
            cls.instances[instance_class][instance.name].append(instance)

    @classmethod
    def write_dict_to_json(input_dict, filename='output.json'):
        serializable_dict = {}
        
        for key, value in input_dict.items():
            if hasattr(value, '__dict__'):
                # Convert the class instance to a dictionary
                serializable_dict[key] = value.__dict__
            else:
                serializable_dict[key] = value
        
        with open(filename, 'w') as f:
            json.dump(serializable_dict, f)

    # @classmethod
    # def save_instances(cls):
    #     for instance_class, second in cls.instances.items():
    #         print(instance_class)
    #         print(second)
    #         if instance_class not in cls.directory:
    #             class_directory = T.os.path.join(cls.directory, instance_class)
    #             T.os.makedirs(class_directory, exist_ok=True)
    #         for sub_instance_class, sub_instances in second.items():
    #             sub_class_directory = T.os.path.join(class_directory, sub_instance_class)
    #             T.os.makedirs(sub_class_directory, exist_ok=True)
    #             for instance in sub_instances:
    #                 filename = T.os.path.join(sub_class_directory, f'{instance.name}.md')
    #                 front_matter = {attr: value for attr, value in instance.__dict__.items() if attr != 'name'}
    #                 # Read the existing content
    #                 if not T.os.path.exists(filename):
    #                     with open(filename, 'w') as file:
    #                         content = f'---\n{T.yaml.dump(front_matter)}---\n'
    #                         file.write(content)
    #                 else:
    #                     with open(filename, 'r') as file:
    #                         content = file.read()
    #                         match = T.re.search(r'---\n(.*?)\n---', content, T.re.DOTALL)
    #                         if match:
    #                             # Update the front matter
    #                             content = content.replace(match.group(0), f'---\n{T.yaml.dump(front_matter)}---\n')
    #                         else:
    #                             # Add the front matter if it doesn't exist
    #                             content = f'---\n{T.yaml.dump(front_matter)}---\n{content}'
    #                     # Write the updated content back to the file
    #                     with open(filename, 'w') as file:
    #                         file.write(content)
    # @classmethod
    # def load_instances(cls):
    #     cls.instances = {'Aliens':{}, 'Planets':{}}
    #     T.CoreRulebookValues.PLANETS = []
    #     T.CoreRulebookValues.ALIEN_TYPES = []
    #     for i, (root, dirs, files) in enumerate(T.os.walk(cls.directory)):
    #         # if root == os.path.join(directory, '*'):
    #         if root == T.os.path.join(cls.directory, 'Aliens'):
    #             T.CoreRulebookValues.ALIEN_TYPES = dirs
    #             for alien in dirs:
    #                 if alien not in cls.instances['Aliens']:
    #                     cls.instances['Aliens'][alien]= []

    #         if root == os.path.join(cls.directory, 'Planets'):
    #             T.CoreRulebookValues.PLANETS = dirs
    #             for planet in dirs:
    #                 if planet not in cls.instances['Planets']:
    #                     cls.instances['Planets'][planet]= []

    #             variable_value = os.path.basename(root)

    #         if root == T.os.path.join(cls.directory, 'Aliens', '*'):
    #             variable_value = T.os.path.basename(root)
    #             for file in files:
    #                 with open(T.os.path.join(root, file), 'r') as f:
    #                     content = f.read()
    #                     match = T.re.search(r'---\n(.*?)\n---', content, T.re.DOTALL)
    #                     if match:
    #                         # Load the front matter
    #                         front_matter = T.yaml.load(match.group(1), Loader=T.yaml.FullLoader)
    #                         # Create an instance of the class
    #                         instance_class_obj = globals()[T.NPC()]
    #                         instance = instance_class_obj(**front_matter)
    #                         Registry.instances['Aliens'][variable_value].append(instance)
    #                     else:
    #                         instance_class_obj = globals()[T.NPC()]
    #                         instance = instance_class_obj()
    #                         Registry.instances['Aliens'][variable_value].append(instance)
            
    #         if root == T.os.path.join(cls._instance.directory, 'Planets', '*'):
    #             variable_value = T.os.path.basename(root)
    #             for file in files:
    #                 with open(T.os.path.join(root, file), 'r') as f:
    #                     content = f.read()
    #                     match = T.re.search(r'---\n(.*?)\n---', content, T.re.DOTALL)
    #                     if match:
    #                         # Load the front matter
    #                         front_matter = T.yaml.load(match.group(1), Loader=T.yaml.FullLoader)
    #                         # Create an instance of the class
    #                         instance_class_obj = globals()[T.NPC()]
    #                         instance = instance_class_obj(**front_matter)
    #                         cls.instances['Aliens'][variable_value].append(instance)
    #                     else:
    #                         instance_class_obj = globals()[T.NPC()]
    #                         instance = instance_class_obj()
    #                         cls.instances['Aliens'][variable_value].append(instance)