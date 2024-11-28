import argparse
from tree_sitter import Language, Parser

# 设置命令行参数解析器
def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse an AIDL file and extract method names.")
    parser.add_argument('aidl_file', type=str, help="Path to the AIDL file to be parsed.")
    return parser.parse_args()

# 解析命令行参数
args = parse_arguments()

# 下载并编译 AIDL 语法（需要下载 AIDL 语法包并编译）
# 这里假设你已经有了 AIDL 的 tree-sitter 语法包
#https://github.com/AndroidIDEOfficial/tree-sitter-aidl.git

# 加载语法库
Language.build_library(
    'build/my-languages.so',
    ['/mnt/Crucial/ljx/git/lang/c++/tree-sitter-aidl']
)

AIDL_LANGUAGE = Language('build/my-languages.so', 'aidl')

# 创建解析器
parser = Parser()

# 设置解析器语言
parser.set_language(AIDL_LANGUAGE)

# 读取并解析 AIDL 文件
with open(args.aidl_file, 'r', encoding='utf-8') as file:
    source_code = file.read()

# 解析源代码
tree = parser.parse(bytes(source_code, 'utf-8'))

# 获取根节点
root_node = tree.root_node

# 提取方法名的递归函数
def extract_methods(node):
    methods = []
    for child in node.children:
        # 查找方法声明节点
        if child.type == 'method_declaration':  # 查找方法声明
            method_name = None
            for sub_child in child.children:
                # 方法名通常是标识符类型的子节点
                if sub_child.type == 'identifier':  
                    method_name = sub_child.text.decode('utf-8')
            if method_name:
                methods.append(method_name)
        # 递归解析所有子节点
        methods.extend(extract_methods(child))
    return methods

# 提取方法名
methods = extract_methods(root_node)

# 输出提取的函数名
for idx, method in enumerate(methods, start=1):
    print(f"{idx}: {method}")
