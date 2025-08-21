# Security Guidelines - HardbanRecords Lab

## Secrets Management

### ✅ DO:
- Store all secrets in environment variables
- Use Render.com Environment tab for production secrets
- Use .env file only for local development (never commit!)
- Use strong, generated SECRET_KEY values
- Rotate API keys regularly

### ❌ DON'T:
- Never commit .env files to Git
- Never put secrets in YAML/JSON config files
- Never share API keys in chat/email
- Never use weak/default passwords

## API Keys Locations:

### Development (.env file - local only):