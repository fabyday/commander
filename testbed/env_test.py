




import os 
os.sys.path.append("..")

import env
if __name__ == "__main__":
    custom_dir_env = env.DirectoryEnvironment(target_path = "D:\\lab\\dataset\\COMA_data", working_directory  = ".\\")
    custom_dir_env.set_options(search_depth = -1).set_target_object(target_name_regex="\w*(.ply)").compile()

    for path_name in custom_dir_env: 
    # for idx, path_name in enumerate(custom_dir_env ): 
        # print(idx, " : ", path_name)
        pass
# 


        
    