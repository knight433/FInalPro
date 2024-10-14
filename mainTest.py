from backend import Backend

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            return text
    
    except FileNotFoundError:
        return f"The file at {file_path} was not found."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
if __name__ == "__main__":
    file_path = 'sample.txt'    
    file_content = read_text_file(file_path)

    obj = Backend()
    obj.video_to_mp3('https://www.youtube.com/watch?v=Hoixgm4-P4M')
    print(obj.sum_up())
