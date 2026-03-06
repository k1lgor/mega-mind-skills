---
name: infra-architect
description: IaC (Terraform, CloudFormation) and Cloud setup. Use for infrastructure design and management.
triggers:
  - "infrastructure"
  - "terraform"
  - "cloudformation"
  - "cloud architecture"
---

# Infra Architect Skill

## Identity

You are an infrastructure architect focused on designing and implementing cloud infrastructure using Infrastructure as Code.

## When to Use

- Designing cloud architecture
- Writing Terraform configurations
- Creating CloudFormation templates
- Planning infrastructure scaling

## Terraform Templates

### Basic AWS Infrastructure

```hcl
# main.tf

provider "aws" {
  region = var.aws_region
}

# VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Project = var.project_name
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# RDS
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"

  allocated_storage     = 20
  max_allocated_storage = 100

  db_name  = "app"
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  skip_final_snapshot     = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot"
}

# ElastiCache
resource "aws_elasticache_cluster" "main" {
  cluster_id           = "${var.project_name}-cache"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"

  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]
}
```

### S3 + CloudFront

```hcl
# Static website hosting

resource "aws_s3_bucket" "website" {
  bucket = "${var.project_name}-website"
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_cloudfront_distribution" "website" {
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = "PriceClass_100"
  http_version        = "http2"

  origin {
    domain_name = aws_s3_bucket_website_configuration.website.website_endpoint
    origin_id   = "s3-website"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3-website"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
```

## Architecture Patterns

### Three-Tier Architecture

```
┌─────────────────────────────────────┐
│           Presentation Tier          │
│  (CloudFront + S3 / API Gateway)    │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│           Application Tier           │
│     (ECS / EKS / Lambda / EC2)      │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│             Data Tier                │
│  (RDS + ElastiCache + S3)           │
└─────────────────────────────────────┘
```

### Microservices Architecture

```
┌────────────────────────────────────────────┐
│                 API Gateway                 │
└─────────┬──────────┬──────────┬───────────┘
          │          │          │
    ┌─────▼────┐┌────▼────┐┌────▼────┐
    │ Service A││Service B││Service C│
    └─────┬────┘└────┬────┘└────┬────┘
          │          │          │
    ┌─────▼────┐┌────▼────┐┌────▼────┐
    │   DB A   ││  DB B   ││  DB C   │
    └──────────┘└─────────┘└─────────┘
```

## Best Practices

1. **Use modules** - Reusable, versioned components
2. **State management** - Remote state with locking
3. **Naming conventions** - Consistent resource naming
4. **Tagging** - Comprehensive resource tagging
5. **Least privilege** - Minimal IAM permissions
6. **Encryption** - Encrypt data at rest and in transit

## Tips

- Use workspaces for multiple environments
- Implement proper state locking
- Use modules for reusable components
- Always use remote state
- Enable logging and monitoring
