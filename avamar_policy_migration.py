import os
import subprocess
print("""
=================================
1 - Exportacion de politicas       |
2 - Transferir archivos exportados |
3 - Importacion de politicas       |
                                   |
                                   |
                                   |
=================================  |
""")


POLICY_FOLDER_PATH = "/tmp/policies"
FILE_PATH = "/tmp/policies/avamar_policies.txt"
cases = input('Que desea hacer: ')

def read_files(file_path, is_export_or_import):
    if (is_export_or_import):

        if file_path:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                for line in lines:
                    slash_pos = line.find('/')
                    if slash_pos == -1:
                        continue

                    col1 = line[:slash_pos].strip()
                    col2 = "/" + line[slash_pos+1:].split()[0]
                    export_commands = "mccli group export --name={}/{}".format(col2, col1)+" --file=/tmp/policies/{}".format(col1)+".xml"
                    
                    print(export_commands)
    else:

        if file_path:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                for line in lines:
                    slash_pos = line.find('/')
                    if slash_pos == -1:
                        continue

                    col1 = line[:slash_pos].strip()
                    col2 = "/" + line[slash_pos+1:].split()[0]
                    export_import = "mccli mcs import --file=/tmp/policies/{}".format(col1)+".xml"+" --target-domain={}".format(col2)+""
                    # export_commands = "mccli group import --file={}/{}".format(col2, col1)+" --file=/tmp/policies/{}".format(col1)+".xml"

                    
                    print(export_import)
def validate_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("El directorio: '{}' ".format(directory)+ "ha sido creado")


def mccli_command_execution(command, is_export_or_import):
    
    with open(FILE_PATH, "w") as file:
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                file.write(stdout)
            else:
                print(stdout)
        except Exception as e:
            print(str(e))

    read_files(FILE_PATH, is_export_or_import)

def case_export():
    try:
        
        all_result = input('Desea obtener el comando de exportacion de politicas de todos los dominios? (Y/N): ')
        validate_directory(POLICY_FOLDER_PATH)
        
        if all_result.lower() == 'y':
            command = ["mccli","group","show","--recursive"]
            mccli_command_execution(command, True)
            
        elif all_result.lower() == 'n':
            result_by_domain = input('Ingrese el dominio que desea exportar las politicas: ')
            command = ["mccli","group","show","--domain="+ result_by_domain]
            mccli_command_execution(command, True)
            
        else:
            print('abortando proceso...')

        

    except Exception as e:
        print("An unexpected error occurred: {}".format(e))


def case_import():
    try:
        all_result = input('Desea obtener el comando de importacion de politicas de todos los dominios? (Y/N): ')
        validate_directory(POLICY_FOLDER_PATH)

        if all_result.lower() == 'y':
            
            command = ["mccli","group","show","--recursive"]
            mccli_command_execution(command, False)

        elif all_result.lower() == 'n':

            result_by_domain = input('Ingrese el dominio que desea exportar las politicas: ')
            command = ["mccli","group","show","--domain="+ result_by_domain]
            mccli_command_execution(command, False)

        else:
            print('abortando proceso...')

    except Exception as e:
        print("An unexpected error occurred: {}".format(e))

def case_migration():

    answer = input('Desea pasar los archivos creados a otro avamar? (Y/N):')

    if answer.lower() == 'y':
        usuario = input('Ingrese el nombre del usuario: ')
        remote_addres = input('Ingrese la direccion IP o nombre del Servidor: ')
        remote_directory = input('Direccion en la cual va a guardar el archivo en el servidor remoto: ')
        file_to_upload = '{}'.format(POLICY_FOLDER_PATH) + '/*xml'
    
        scp_command = 'scp {} {}@{}:{}'.format(file_to_upload,usuario,remote_addres,remote_directory)
    
        print(scp_command)
        os.system(scp_command)
    else:
        pass

def default_case():
    return "Default case"

switch_dict = {
    1: case_export,
    2: case_migration,
    3: case_import
}

def switch_example(value):
    return switch_dict.get(value, default_case)()

result = switch_example(int(cases))

