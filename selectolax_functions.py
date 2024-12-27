from selectolax.lexbor import LexborHTMLParser
import re

def xpath_to_css(xpath):
    """
    Converts a simple XPath expression to a CSS selector.
    Handles basic XPath expressions including attributes and the '//' operator.
    """
    xpath = xpath.strip()
    tokens = re.split(r'(//|/)', xpath)
    css_parts = []
    combinator = ''
    first = True
    for token in tokens:
        token = token.strip()
        if token == '/':
            combinator = ' > '
        elif token == '//':
            combinator = ' '
        elif token:
            # Handle tag and optional predicates
            # Match tag with optional predicates
            match = re.match(r'^([a-zA-Z0-9\-\*]+)(\[(.*?)\])?$', token)
            if match:
                tag = match.group(1)
                predicates = match.group(3)  # May be None
                css_selector = tag if tag != '*' else '*'
                if predicates:
                    # Split predicates by ' and ' (not handling 'or' here)
                    predicates_list = re.findall(r'\[@([^=\]]+)=["\']([^"\']+)["\']\]', '[' + predicates + ']')
                    for attr_name, attr_value in predicates_list:
                        if attr_name == 'id':
                            css_selector += f'#{attr_value}'
                        elif attr_name == 'class':
                            css_selector += f'.{attr_value}'
                        else:
                            css_selector += f'[{attr_name}="{attr_value}"]'
                    # Handle positional predicates [n]
                    pos_match = re.match(r'^\d+$', predicates)
                    if pos_match:
                        index = int(predicates)
                        css_selector += f':nth-of-type({index})'
                    # Handle wildcard index [*] (which selects all elements, so no change needed)
                    elif predicates == '*':
                        pass
                if first:
                    css_parts.append(css_selector)
                    first = False
                else:
                    css_parts.append(combinator + css_selector)
                combinator = ''
            else:
                # Handle cases where the token doesn't match expected pattern
                pass
    css_selector = ''.join(css_parts).strip()
    return css_selector

def find_elements_by_xpath(html_content, xpath_str):
    """
    Finds all elements in the HTML content that match the given XPath.
    """
    parser = LexborHTMLParser(html_content)
    css_selector = xpath_to_css(xpath_str)
    return parser.css(css_selector)

def find_element_by_xpath(html_content, xpath_str):
    """
    Finds the first element in the HTML content that matches the given XPath.
    """
    parser = LexborHTMLParser(html_content)
    css_selector = xpath_to_css(xpath_str)
    return parser.css_first(css_selector)

def find_elements_by_css(html_content, css_selector):
    """
    Finds all elements in the HTML content that match the given CSS selector.
    """
    parser = LexborHTMLParser(html_content)
    return parser.css(css_selector)

def find_element_by_css(html_content, css_selector):
    """
    Finds the first element in the HTML content that matches the given CSS selector.
    """
    parser = LexborHTMLParser(html_content)
    return parser.css_first(css_selector)

# Example Usage
if __name__ == "__main__":
    html_content = '''
    <html>
        <head>
            <title>Sample Page</title>
            <script src="app.js"></script>
        </head>
        <body>
            <div id="main">
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                    <li>Item 3</li>
                </ul>
                <ul>
                    <li>Item A</li>
                    <li>Item B</li>
                </ul>
                <section>
                    <div>
                        <p>Nested Paragraph</p>
                    </div>
                </section>
            </div>
            <footer>
                <p>Footer Content</p>
            </footer>
        </body>
    </html>
    '''

    # Using XPath functions
    xpath_single = "/html/body/div/ul/li[2]"
    result_single = find_element_by_xpath(html_content, xpath_single)
    if result_single:
        print(f"Single Element Found using XPath: {result_single.text(strip=True)}")
    else:
        print("Single Element Not Found using XPath.")

    # Using CSS functions
    css_selector = "html > body > div > ul > li:nth-of-type(2)"
    result_single_css = find_element_by_css(html_content, css_selector)
    if result_single_css:
        print(f"Single Element Found using CSS: {result_single_css.text(strip=True)}")
    else:
        print("Single Element Not Found using CSS.")

    # Multiple Elements Query using XPath
    xpath_multiple = "/html/body/div/ul/li"
    result_multiple = find_elements_by_xpath(html_content, xpath_multiple)
    print("\nMultiple Elements Found using XPath:")
    for elem in result_multiple:
        print(f"- {elem.text(strip=True)}")

    # Multiple Elements Query using CSS
    css_multiple = "html > body > div > ul > li"
    result_multiple_css = find_elements_by_css(html_content, css_multiple)
    print("\nMultiple Elements Found using CSS:")
    for elem in result_multiple_css:
        print(f"- {elem.text(strip=True)}")

    # Wildcard Query using XPath
    xpath_wildcard = "/html/body//div"
    result_wildcard = find_elements_by_xpath(html_content, xpath_wildcard)
    print("\nWildcard Elements Found using XPath:")
    for elem in result_wildcard:
        print(f"- {elem.tag}: {elem.text(strip=True)}")

    # Wildcard Query using CSS
    css_wildcard = "html > body div"
    result_wildcard_css = find_elements_by_css(html_content, css_wildcard)
    print("\nWildcard Elements Found using CSS:")
    for elem in result_wildcard_css:
        print(f"- {elem.tag}: {elem.text(strip=True)}")

    # Nested Wildcard Query using XPath
    xpath_nested_wildcard = "/html/body//section//div//p"
    result_nested_wildcard = find_elements_by_xpath(html_content, xpath_nested_wildcard)
    print("\nNested Wildcard Elements Found using XPath:")
    for elem in result_nested_wildcard:
        print(f"- {elem.tag}: {elem.text(strip=True)}")

    # Nested Wildcard Query using CSS
    css_nested_wildcard = "html > body section div p"
    result_nested_wildcard_css = find_elements_by_css(html_content, css_nested_wildcard)
    print("\nNested Wildcard Elements Found using CSS:")
    for elem in result_nested_wildcard_css:
        print(f"- {elem.tag}: {elem.text(strip=True)}")
