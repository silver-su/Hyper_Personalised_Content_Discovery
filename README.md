# Details

**Project** : Hyper-personalised Content Discovery  
**Team Number** : _insert team number here_  
**Team Name** : Cathlon Lau, Steven Guo, Silver Su  
**Demonstration Video** : <https://drive.google.com/file/d/1wNleg6WoDnxHY9_H-5qoj2V6QGJ_B_FF/view>  

# Overview

This project serves as a groundbreaking demonstration of how Generative AI, integrated with MongoDB Atlas Developer Data Platform, can revolutionize the OTT platform user experience by enabling advanced content search and hyper-personalized recommendations.

# Justification

## Current State

Existing OTT platform use traditional approach to recommendation such as machine learning model. Leverage Generative AI to improve recommendation engine, make it more personalization.

## Solution

Utilize MongoDB Atlas and its Developer Data Platform to manage and analyze essential data types, such as raw content metadata, user search history, user digital footprints, and browsing behavior. Implement Generative AI to use this data for creating dynamic keywords and hyper-personalized content recommendations.

# Detailed Application Overview

_Describe the architecture of your application and include a diagram._
_List all the MongoDB components/products used in your demonstration._
_Describe what you application does and how it works_


# Roles and Responsibilities

- Cathlon Lau, team leader to organize team member to initiate this ideal.
- Steven Guo, contruct whole architecture and prepare the deliverable.
- Silver Su, implement sample code for demo.

# Demonstration Script

<!-- _Demonstration script (or link to script) goes here_

_The demonstration script should provide all the information required for another MongoDB SA to deliver your demonstration to a prospect. This should include:_

* _setup/installation steps_
* _step by step instructions on how to give the demonstration_
* _key points to emphasize at each point in the demonstration_
* _any tear down steps required to reset the demonstration so it is ready for the next time_ -->

## Prerequisites

### OS Environment Preparation

- RHEL
  
  ```ssh
  sudo yum install cmake
  sudo yum install gcc-c++
  ```

- Mac M1
  
  ```ssh
  brew install cmake
  brew install libpng
  ```

### Application Preparation

- Anaconda, <https://www.anaconda.com/>
  
- Install Python library by Anaconda
  
  ```sh
  conda env create -f environment.yaml
  ```

## Data Preparation

### Atlas Cluster Information

> Create your own Atlas cluster, input connection string into *src/config.py*, change the value of **MDB_URL** in *src/config.py*

### Import Sample Data

- Image Search for movie star
  
  There are some of sample movie star picture in *src/static/movie_star*. If you would like to add new picture, filename is the name of movie star and content will be the facial image.

  Execute importer program.

  ```sh
  conda activate demo
  python src/movie_star_importer.py
  ```

- Text to Image Search for food
  
  There are some of sample food picture in *src/static/food*. If you would like to add new picture, filename is the name of food and content will be the food image.

  Execute importer program.

  ```sh
  conda activate demo
  python src/food_importer.py
  ```

### Create Vector Index

- Image Search for movie star
  
  Create Vector Index named **faces** in Atlas UI with following specification.

  ```json
  {
    "fields": [
      {
        "numDimensions": 128,
        "path": "embeddings",
        "similarity": "euclidean",
        "type": "vector"
      }
    ]
  }
  ```

- Text to Image Search for food
  
  Create Vector Index named **food_idx** in Atlas UI with following specification.

  ```json
  {
    "fields": [
      {
        "numDimensions": 512,
        "path": "embeddings",
        "similarity": "euclidean",
        "type": "vector"
      }
    ]
  }
  ```

## Launch Application

Activate Anaconda environment, start web service and listen on 8000 port.

```sh
conda activate demo
bin/start.sh
```

Once application started, you could access following URL to test it.

- <http://[IP]:8000> for Image Search for movie star
- <http://[IP]:8000/food> for Text to Image Search for food