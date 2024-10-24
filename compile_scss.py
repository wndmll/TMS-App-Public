import os
import sass

# Paths for SCSS and CSS files
scss_dir = 'app/static/css/scss/'
css_dir = 'app/static/css'

# Compile SCSS to CSS
def compile_scss():
    scss_files = [
        os.path.join(scss_dir, 'main.scss'),  # Entry point SCSS file
    ]
    
    for scss_file in scss_files:
        css_file = os.path.join(css_dir, 'main.css')  # Output CSS file

        # Compile SCSS to CSS
        with open(css_file, 'w') as f:
            css_content = sass.compile(filename=scss_file)
            f.write(css_content)
            print(f'Compiled {scss_file} to {css_file}')

if __name__ == '__main__':
    compile_scss()