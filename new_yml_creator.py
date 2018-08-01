import os

#read function
def read_file(filename):
    try:
        file=open(filename,"r")
        file_content=file.read()
        file.close()
        return file_content
    except EnvironmentError as e:
        print("File operation failed\nError: %s" % e)
        return -1

#line counter function
def total_lines(file_content):
    try:
        lines=[]
        line_in_file=file_content.split("\n")
        number_of_lines=len(line_in_file)
        lines.append(line_in_file)
        return number_of_lines,lines
    except EnvironmentError as e:
        print("File operation failed\nError: %s" % e)
        return "",-1

#file creator function
def create_file(total_lines,line,filename):
    try:
        file=open(filename,"a")
        print("length=",total_lines)
        job_id=1
        count=0
        while job_id<(total_lines+1):
            file.write("\njob "+ str(job_id) +":\n  <<: * job_definition\n  script:\n    - "+line[0][count]+"\n")
            count+=1
            job_id+=1
        job_id=0
        count=0
        return 0
    except EnvironmentError as e:
        print("File operation failed\nError: %s" % e)
        return -1

#Main function
def main():
    line=[]
    #specify filename to read the content from
    filename=".test.txt"
    #specify new_file(name) in which the syntax will be added to
    new_file="gitlab-ci.yml"
    content=read_file(filename)
    if(content==-1):
        print("Error reading file.")
        os._exit(1)
    number_of_lines,line=total_lines(content)
    if(line==-1):
        print("Error reading line numbers.")
        os._exit(1)
    err=create_file(number_of_lines,line,new_file)
    if(err==-1):
        print("Error while creating file.")
        os._exit(1)
    else:
        print("Successfully completed tasks.")

if __name__ == '__main__':
    main()
