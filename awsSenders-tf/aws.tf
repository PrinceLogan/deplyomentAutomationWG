provider "aws" {
  region     = "us-west-2"
  access_key = "my-access-key"
  secret_key = "my-secret-key"
}

resource "aws_instance" "example" {
ami = "ami-83a713e0"
instance_type = "t2.micro"
tags {
Name = "your-instance"
}
}
