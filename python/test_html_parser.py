from html_parser import HtmlParser, PrintHtml


class HtmlParserApp:
    @staticmethod
    def main():
        parser = HtmlParser(iter(ExampleHtml.value))
        content = parser.parse()
        print(content)
        print("\n\n==========================\n")
        print(PrintHtml.apply(content))


class ExampleHtml:
    value = """
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Example HTML</title>
            <style>
                /* Add some CSS styles here if needed */
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
            </style>
        </head>
        <body>

            <h1 id="main-heading" class="header">Welcome to Example HTML</h1>

            <p>This is a simple example of HTML with some common attributes:</p>

            <ul>
                <li><a href="https://www.example.com" target="_blank" title="Visit Example">Visit Example</a></li>
                <li><img src="example-image.jpg" alt="Example Image" width="300" height="200"></li>
            </ul>

            <form action="/submit" method="post">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
                <br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <br>
                <input type="submit" value="Submit">
            </form>

            <script>
                // Add some JavaScript code here if needed
                console.log("Hello, this is JavaScript!");
            </script>

        </body>
        </html>
    """


# Run the application
HtmlParserApp.main()
