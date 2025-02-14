# Blog Template

[![Lint and Test](https://github.com/sedexdev/blog_template/actions/workflows/test.yml/badge.svg)](https://github.com/sedexdev/blog_template/actions/workflows/test.yml)

Template for your new Flask blog!

## Read the guide on my blog

[Build a Flask blog Part 1](https://www.sedexdev.co.uk/build_a_flask_blog_part_1)
[Build a Flask blog Part 2](https://www.sedexdev.co.uk/build_a_flask_blog_part_2)
[Build a Flask blog Part 3](https://www.sedexdev.co.uk/build_a_flask_blog_part_3)

## Hosting

[Pythonanywhere](https://www.pythonanywhere.com/)

The Flask app will be served from an AWS backend via the cloud hosting PaaS platform <b>Pythonanywhere</b>

By following the guide you will configure:

-   A basic Flask app with TailwindCSS
-   JSON data storage to save costs on databases
-   Custom DNS</br>
-   Auto-renewing SSL via Let's Encrypt</br>
-   A virtual environment for your application</br>
-   An SSH key into your Pythonanywhere instance from GitHub to allow GitOps automation</br>

## Workflow

To update the site you will do the following:

-   Use the <code>scripts/newpost.sh</code> script to create a new post template with metadata and routing</br>
-   Use the <code>scripts/updatepost.sh</code> script to modify post metadata</br>
-   Develop and test locally</br>
-   Run linting/auditing/testing via GitHub Actions</br>
-   Once ready to go live push app changes with the message '[update]' in the commit
-   A GitHub Webhook endpoint in your app will be triggered to force a remote pull from your repo on the PythonAnywhere server
-   Your server will reload with the changes reflected almost immediately

## License

[MIT](https://github.com/sedexdev/sedexdevblog/blob/main/LICENSE)
