# Item Catalog

An application that provides a list of items within a variety of categories

## Prerequisites

Please make sure that following softwares are install into your system

```
Python preferably 2.7.9
```
```
Oracle VM
```
```
Vagrant
```

## How To Run

```
1. Install Vagrant and VirtualBox
2. Download or clone from https://github.com/udacity/fullstack-nanodegree-vm
3. Find the catalog folder and replace it with the content of https://github.com/priyankasingh2210/Priyanka_ItemCatelog
4. Go to the directory where you have donloaded https://github.com/udacity/fullstack-nanodegree-vm and change to the directory vagrant/catalog
5. Run command vagrant up
6. Run command vagrant ssh
7. change the directory to /vagrant/catalog
8. Run command python database_setup.py to create itemCatelog.db if it doesn't exist already
9. Run command python categoriesanditems.py to populate itemCatelog.db if it is not already populated
10. Now run the main application called catelogApplication.py to start the server and run the itemCatelog website
11. Run http://localhost:5000 to launch item catalog website
```

## Authors

* **Priyanka Singh** 

## Acknowledgments

* A big thank you to Udacity's full stack nanodegree program


