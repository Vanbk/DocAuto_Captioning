import make_caption

file_path="/Users/soyeonkim/PycharmProjects/team_project/"
store_path="/Users/soyeonkim/PycharmProjects/team_project/"
file_name="test.docx"
output_captions=["two childrens are playing", "a squirrel eats"]


make_caption.extractImg(file_path, file_name, store_path)
make_caption.changeCaption(file_path,file_name, output_captions)