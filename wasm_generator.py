class WasmGenerator:
    def __init__(self, parsed_code):
        self.code = '(module \n'\
                     '(func $~write_i (import "imports" "write") (param i64)) \n'\
                     '(func $~write_f (import "imports" "write") (param f64)) \n'

        for procedure in parsed_code['procedures']:
            self.code += f'(func {procedure["name"]} \n'
            self.extract_variables(procedure['args'], 'param')
            self.extract_variables(procedure['locals'], 'local')
            self.code += ") \n"

        main = parsed_code['main']
        self.code += '(func $main \n'
        self.extract_variables(main['locals'], 'local')
        self.code += ") \n"
        self.code += '(export "main" (func $main)) \n'
        self.code += ") \n"

    def extract_variables(self, var_list, var_type):
        extracted = [f"({var_type} ${var['name']} {var['type']})" for var in var_list]
        if extracted:
            self.code += f"{' '.join(extracted)} \n"