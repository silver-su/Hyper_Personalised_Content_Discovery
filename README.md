# Details

**Project** : Hyper-personalised Content Discovery  
**Team Number** : _insert team number here_  
**Team Name** : Cathlon Lau, Steven Guo, Silver Su  
**Demonstration Video** : _Insert link to demonstration video_  

# Overview

To revolutionize the OTT platform’s user experience by integrating Generative AI with MongoDB Atlas for advanced content search and personalized recommendations.

# Justification

## Current State
Existing OTT platform use tranditional approach to recommendation such as machine learning model. Leverage Generative AI to improve recommendation engine, make it more personalization.

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

### Start Application

Activate Anaconda environment, start web service.

```sh
conda activate demo
bin/start.sh
```
