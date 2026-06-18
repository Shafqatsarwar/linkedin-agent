# LinkedIn Agent — Claude.ai Artifact Version

This version runs entirely inside Claude.ai as an interactive artifact.
No Python backend, no server, no deployment needed.

## How to use
1. Open this conversation in Claude.ai
2. The widget renders inline — just click "Generate draft"
3. Copy the approved post and paste it into LinkedIn manually

## Limitations vs the laptop version
| Feature | Claude artifact | Laptop version |
|---------|-----------------|-----------------|
| Draft posts with AI | Yes | Yes |
| Human approval step | Yes | Yes |
| Auto-publish to LinkedIn | No (copy-paste) | Yes (direct API) |
| LinkedIn OAuth login | No | Yes |
| Profile improver | No | Yes |
| Runs without install | Yes | No (needs Python) |
| Uses Claude quota | Yes | No |

## Why no auto-publish here
Claude.ai's sandbox cannot make outbound authenticated calls to LinkedIn's
OAuth-protected API or hold a persistent login session. It CAN call Gemini
directly (stateless API call), so drafting works, but publishing requires
the laptop version's Python backend with real OAuth tokens.

## Recreating the artifact
Ask Claude in any conversation:
"Build me the LinkedIn post drafter artifact with the colourful 
project diagram and Gemini draft generator"

Or paste the saved HTML/JS from this folder into a new Claude chat 
and ask Claude to render it as an HTML artifact.
