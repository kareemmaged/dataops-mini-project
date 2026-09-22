# DataOps Mini Project

Automated data pipeline demonstrating DataOps practices: Python transformation,
pytest testing, Docker containerization, GitHub Actions CI, and Terraform-managed
local Docker infrastructure.

## Structure
- `src/transform.py` — cleans, validates, and aggregates transaction data
- `tests/test_transform.py` — pytest suite
- `Dockerfile` — containerizes the pipeline
- `terraform/` — manages the Docker image/container via the kreuzwerker/docker provider
- `.github/workflows/ci.yml` — CI: pytest → Docker build → Terraform validate

## Run locally

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest -v
python src/transform.py
```

## Run with Docker

```bash
docker build -t dataops-pipeline .
docker run --name dataops-pipeline-container dataops-pipeline
```

## Run with Terraform

```bash
cd terraform
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
# ...
terraform destroy
```