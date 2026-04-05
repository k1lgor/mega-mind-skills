---
name: infra-architect
compatibility: Antigravity, Claude Code, GitHub Copilot
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

## When NOT to Use

- Application-level concerns (business logic, API design, data models) — use `backend-architect` or `api-designer` instead
- Local developer tooling setup (Docker Compose for dev, local environment scripts) — use `docker-expert` for container setup
- CI/CD pipeline configuration — use `ci-config-helper` instead
- Kubernetes-specific workload orchestration — use `k8s-orchestrator` instead

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

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| IAM role over-provisioned with admin wildcard, violating least-privilege | Role created with `"Action": "*"` or `"Resource": "*"` as a quick workaround during development and never tightened | Run `tfsec` or `checkov` to flag wildcard IAM policies; replace with the minimum required actions and specific resource ARNs |
| Terraform state stored locally, diverges between team members | No remote backend configured; each developer has a different `.tfstate` file on their machine | Migrate to remote state (S3 + DynamoDB lock or Terraform Cloud); run `terraform state pull` to reconcile, then enforce with CI |
| Security group allows 0.0.0.0/0 ingress on port 22 | SSH port opened to the world for convenience during initial setup; never restricted | Remove the `0.0.0.0/0` ingress rule; restrict SSH to a bastion host CIDR or use AWS Systems Manager Session Manager instead |
| No automated backup policy on stateful resource | RDS `backup_retention_period` left at 0 or ElastiCache/S3 versioning not enabled | Set `backup_retention_period >= 7` on RDS; enable S3 versioning and object lock; verify with `terraform plan` that changes apply |
| DNS propagation delay causes downtime during blue-green cutover | TTL on DNS record is too high (e.g., 3600s) and old record cached during cutover | Set DNS TTL to 60s at least 1 hour before cutover; after cutover confirm new endpoint is live before removing old stack |

## Anti-Patterns

- Never store Terraform state locally on a developer machine because local state is not shared between team members, causing concurrent `terraform apply` runs to diverge, corrupt resources, or create duplicate infrastructure.
- Never attach `AdministratorAccess` or equivalent wildcard policies to application IAM roles because over-permissioned roles expand the blast radius of a credential compromise from one service to the entire AWS account.
- Never create cloud resources manually through the console and then import them into Terraform because manual creation breaks the IaC audit trail, and the imported state often diverges from the actual resource on the next plan, causing unexpected diffs or resource replacement.
- Never skip resource tagging on production infrastructure because untagged resources cannot be attributed to a team or cost center, making chargeback allocation impossible and allowing orphaned resources to accumulate and inflate the cloud bill undetected.
- Never open security group rules to `0.0.0.0/0` on non-public-facing ports because any internet-accessible service exposed without need becomes an attack surface; a single misconfiguration can expose internal APIs, databases, or management ports.
- Never run `terraform apply` in a CI pipeline without a prior `terraform plan` review step because an unreviewed apply can destroy production resources when upstream module versions change or when a refactor renames a resource without a `moved` block.
- Never use the default VPC for production workloads because the default VPC has permissive default security groups and no network segmentation, meaning any new resource provisioned without explicit security group assignment is accessible to all other resources in the account.

## Self-Verification Checklist

- [ ] `terraform validate` exits 0 on all changed modules
- [ ] `terraform plan` exits 0 and shows no unintended resource replacements (0 destroys of production resources that are not explicitly intended)
- [ ] `tfsec` or `checkov` passes with 0 HIGH severity findings on all changed Terraform files
- [ ] Terraform state is stored remotely (S3 + DynamoDB lock, or equivalent) — never local `terraform.tfstate`
- [ ] All IAM roles follow least-privilege principle: only the specific actions and resources needed are granted
- [ ] All secrets and credentials are stored in AWS Secrets Manager / SSM Parameter Store — no hardcoded values in `.tf` files
- [ ] Resources are tagged with at minimum: `Project`, `Environment`, and `ManagedBy = terraform`

## Success Criteria

This task is complete when:
1. `terraform plan` shows zero errors and the planned changes match the intended architecture
2. All resources are defined in reusable modules with documented variables and outputs
3. The infrastructure has been applied to a non-production environment and verified to function correctly
