## VPC and Network Setup

In this section, we will create the networking infrastructure required for the application. The web server will be deployed inside a public subnet while the MySQL database will remain isolated inside private subnets.

Network Architecture

The infrastructure consists of:

- 1 Virtual Private Cloud (VPC)
- 2 Public Subnets
- 2 Private Subnets
- 1 Internet Gateway
- 2 Route Tables
- Security Groups for EC2 and RDS

This design follows AWS best practices by ensuring that only the web server is publicly accessible while the database remains private.

## Step 1: Create a VPC

From the AWS Console, search for **VPC**.

Select **Create VPC**.

Choose **VPC only** and configure:

  | Setting  |   Value |
  |-----------| -------------------|
  | Name        | python-webapp-vpc|
  | IPv4 CIDR |  10.0.0.0/16 |
  | IPv6     |   None |
  | Tenancy    | Default |

Click **Create VPC**.

## Step 2: Create an Internet Gateway

Create an Internet Gateway named **python-webapp-igw** and attach it to your VPC.

## Step 3: Create Subnets

Create two public subnets.

 | Name            |  AZ        |  CIDR|
 | -----------------| -----------| -------------|
 | public-subnet-1  | First AZ   | 10.0.1.0/24|
 | public-subnet-2  | Second AZ  | 10.0.3.0/24|

 Enable **Auto-assign public IPv4 address** on both public subnets.

Create Private Subnets

  |Name              | AZ        |  CIDR|
  |------------------ |-----------| -------------|
  |private-subnet-1  | First AZ   | 10.0.2.0/24|
 | private-subnet-2  | Second AZ  | 10.0.4.0/24|


## Step 4: Create Route Tables

### Public Route Table

Associate with both public subnets and Add a route:

  |Destination   |Target|
  |------------- |------------------|
 | 0.0.0.0/0  |   Internet Gateway|

### Private Route Table

Associate with both private subnets to the private route table.


## Step 5: Create Security Groups

### Web Server Security Group

Inbound:

  | Type   | Port |  Source | 
  | -------| ------ | -----------| 
  | SSH    | 22    | Your IP/32 |
  | HTTP   | 80   |   0.0.0.0/0 |
  | HTTPS  | 443   | 0.0.0.0/0 |
  | MYSQL/Aurora | 3306 | 0.0.0.0/0 |
  | Custom TCP | 5000 | 0.0.0.0/0 |

Outbound: Allow all.

### Database Security Group

Inbound:

  | Type  |  Port  | Source |
  | ------- | ------ | ---------------|
  | MySQL   | 3306   | web-server-sg |

Outbound: Allow all.
