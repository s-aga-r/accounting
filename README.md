# **Accounting**

An Accounting App with a double-entry accounting system built on [Frappe](https://frappeframework.com/).

## **Table of Contents :**
* [Installation](#installation)
* [How to Run?](#how-to-run)
* [Portal Pages](#portal-pages)
* [License](#license)

## **Installation**

From [bench](https://frappeframework.com/docs/user/en/tutorial/install-and-setup-bench) directory :
  ```bash
  bench get-app https://github.com/s-aga-r/Accounting
  env/bin/pip install -r apps/accounting/requirements.txt
  bench new-site accounting
  bench --site accounting install-app accounting
  ```
## **How to Run ?**
  ```bash
  bench --site accounting add-to-hosts
  bench start
  ```
  Now you can access your site at http://accounting:8000.

## **Portal Pages :**
* ### **Home**
  ![Home](https://user-images.githubusercontent.com/63660334/139655192-0a89709a-3be8-4050-bdfa-e834239fe8c2.png)
* ### **Products**
  ![Products](https://user-images.githubusercontent.com/63660334/139655213-4c093a1b-bcfd-4cac-ae73-80d731def917.png)
* ### **Cart**
  ![Cart](https://user-images.githubusercontent.com/63660334/139655225-96fdb7a8-8a58-47ae-9e4d-749e7d80ae70.png)
  ### **Invoice**
  ![Invoice](https://user-images.githubusercontent.com/63660334/139655231-6d9fdd96-3917-4df4-bae7-a588ba3524da.png)
* ### **About Us**
  ![About Us](https://user-images.githubusercontent.com/63660334/139655237-ef885230-4528-4d5b-bcb4-6fa66c2de105.png)
* ### **Desk**
  ![Desk](https://user-images.githubusercontent.com/63660334/139655255-dc97564b-05f3-4bec-aa8c-b28c39df74e4.png)
















## License
This repository has been released under the [MIT License](license.txt).