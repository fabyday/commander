




import os 
os.sys.path.append("..")

import argsparser as ap
if __name__ == "__main__":
    parser = ap.BaseArgsParser()
    parser.compile()
    print(parser.get_data())


        
    