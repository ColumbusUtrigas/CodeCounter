import os
import sys

codelines = {}
codelines['ActionScript'] = [[], 0]
codelines['Ada']          = [[], 0]
codelines['Assembler']    = [[], 0]
codelines['Basic']        = [[], 0]
codelines['C']            = [[], 0]
codelines['C header']     = [[], 0]
codelines['C++']          = [[], 0]
codelines['C++ header']   = [[], 0]
codelines['C#']           = [[], 0]
codelines['Cg']           = [[], 0]
codelines['Cobol']        = [[], 0]
codelines['CoffeeScript'] = [[], 0]
codelines['Coq']          = [[], 0]
codelines['CUDA']         = [[], 0]
codelines['D']            = [[], 0]
codelines['ECMAScript']   = [[], 0]
codelines['Erlang']       = [[], 0]
codelines['F#']           = [[], 0]
codelines['Fortran']      = [[], 0]
codelines['Go']           = [[], 0]
codelines['GLSL']         = [[], 0]
codelines['Groovy']       = [[], 0]
codelines['Haskell']      = [[], 0]
codelines['HLSL']         = [[], 0]
codelines['HTML']         = [[], 0]
codelines['Java']         = [[], 0]
codelines['JavaScript']   = [[], 0]
codelines['JSON']         = [[], 0]
codelines['Kotlin']       = [[], 0]
codelines['LaTeX']        = [[], 0]
codelines['Lisp']         = [[], 0]
codelines['Lua']          = [[], 0]
codelines['Objective-C']  = [[], 0]
codelines['OCaml']        = [[], 0]
codelines['OpenCL']       = [[], 0]
codelines['Pascal']       = [[], 0]
codelines['Perl']         = [[], 0]
codelines['Perl 6']       = [[], 0]
codelines['PHP']          = [[], 0]
codelines['PostScript']   = [[], 0]
codelines['Python']       = [[], 0]
codelines['Q']            = [[], 0]
codelines['Q#']           = [[], 0]
codelines['Ruby']         = [[], 0]
codelines['Rust']         = [[], 0]
codelines['Scala']        = [[], 0]
codelines['Swift']        = [[], 0]
codelines['TypeScript']   = [[], 0]

langs = {}
langs[('.as')]                         = codelines['ActionScript'][0]
langs[('.adb', 'ads')]                 =  codelines['Ada'][0]
langs[('.asm', '.masm', '.nasm')]      = codelines['Assembler'][0]
langs[('.bas')]                        = codelines['Basic'][0]
langs[('.c')]                          = codelines['C'][0]
langs[('.h')]                          = codelines['C header'][0]
langs[('.cpp', '.cxx', '.c++', '.cc')] = codelines['C++'][0]
langs[('.hpp', '.hxx', '.h++', '.hh')] = codelines['C++ header'][0]
langs[('.cs')]                         = codelines['C#'][0]
langs[('.cg')]                         = codelines['Cg'][0]
langs[('.cbl', '.cob', '.cpy')]        = codelines['Cobol'][0]
langs[('.coffee', '.litcoffee')]       = codelines['CoffeeScript'][0]
langs[('.v')]                          = codelines['Coq'][0]
langs[('.cu', '.cuh', '.cuda')]        = codelines['CUDA'][0]
langs[('.d')]                          = codelines['D'][0]
langs[('.es')]                         = codelines['ECMAScript'][0]
langs[('.erl', '.hrl')]                = codelines['Erlang'][0]
langs[('.fs', '.fsi', '.fsx')]         = codelines['F#'][0]
langs[('fsscript')]                    = codelines['F#'][0]
langs[('.f', '.for', '.f90')]          = codelines['Fortran'][0]
langs[('.go')]                         = codelines['Go'][0]
langs[('.glsl')]                       = codelines['GLSL'][0]
langs[('.groovy')]                     = codelines['Groovy'][0]
langs[('.hs', '.lhs')]                 = codelines['Haskell'][0]
langs[('.hlsl')]                       = codelines['HLSL'][0]
langs[('.html')]                       = codelines['HTML'][0]
langs[('.java')]                       = codelines['Java'][0]
langs[('.js', '.mjs')]                 = codelines['JavaScript'][0]
langs[('.json')]                       = codelines['JSON'][0]
langs[('.kt', '.kts')]                 = codelines['Kotlin'][0]
langs[('.tex')]                        = codelines['LaTeX'][0]
langs[('.lsp')]                        = codelines['Lisp'][0]
langs[('.lua')]                        = codelines['Lua'][0]
langs[('.m', '.mm')]                   = codelines['Objective-C'][0]
langs[('.ml', '.mli')]                 = codelines['OCaml'][0]
langs[('.cl')]                         = codelines['OpenCL'][0]
langs[('.pp', '.pas')]                 = codelines['Pascal'][0]
langs[('.pl', '.pm', '.t', '.pod')]    = codelines['Perl'][0]
langs[('.p6', '.pl6', '.pm6')]         = codelines['Perl 6'][0]
langs[('.php', '.phtml', '.php3')]     = codelines['PHP'][0]
langs[('.php4', '.php5', '.php7')]     = codelines['PHP'][0]
langs[('.phps', '.php-s', '.pht')]     = codelines['PHP'][0]
langs[('.ps')]                         = codelines['PostScript'][0]
langs[('.py')]                         = codelines['Python'][0]
langs[('.q')]                          = codelines['Q'][0]
langs[('.qs')]                         = codelines['Q#'][0]
langs[('.rb')]                         = codelines['Ruby'][0]
langs[('.rs', '.rlib')]                = codelines['Rust'][0]
langs[('.sc', '.scala')]               = codelines['Scala'][0]
langs[('.swift')]                      = codelines['Swift'][0]
langs[('.ts', '.tsx')]                 = codelines['TypeScript'][0]

def Folders(args):
	folders_list = []

	if len(args) is 0:
		folders_list.append('.')
	else:
		for folder_name in args:
			if os.path.isdir(folder_name):
				folders_list.append(folder_name)
			else:
				print('Error:', folder_name, 'is not a directory')
				sys.exit()

	return folders_list

def FilesInFolder(path, recursive):
	files_list = []

	if recursive is True:
		for root, dirs, files in os.walk(path):
			for filename in files:
				files_list.append(filename)
	else:
		files_list = os.listdir(path)

	return files_list

def LinesInLang(lang):
	for file in codelines[lang][0]:
		codelines[lang][1] += sum(1 for line in open(file))

arguments = sys.argv[1:]

folders = Folders(arguments)

for folder in folders:

	files = FilesInFolder(folder, True)

	for file in files:
		for extension in langs:
			if file.lower().endswith(extension):
				langs[extension].append(file)

	total_lines = int(0)

	for lang in codelines:
		LinesInLang(lang)

		total_lines += codelines[lang][1]

		if codelines[lang][1] is not 0:
			print(lang + ':', codelines[lang][1])

	print('')
	print('Total:', total_lines)






