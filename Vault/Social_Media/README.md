# Social Media Vault

This folder contains all social media content, analytics, and archives for the AI Employee's multi-platform social presence.

## Folder Structure

```
Social_Media/
├── LinkedIn/          # Professional B2B content (Silver Tier)
├── Facebook/          # Community engagement (Gold Tier)
├── Instagram/         # Visual storytelling (Gold Tier)
├── Twitter/           # Real-time thought leadership (Gold Tier)
└── README.md          # This file
```

## Platform Overview

### LinkedIn (Silver Tier)
- **Target:** B2B professionals, decision-makers
- **Content:** Industry insights, professional updates, long-form posts
- **Frequency:** 2-3 posts per week
- **Skill:** `post-to-linkedin`

### Facebook (Gold Tier)
- **Target:** Community, broader audience
- **Content:** Behind-the-scenes, company updates, community engagement
- **Frequency:** 3-5 posts per week
- **Skill:** `post-to-social-media`

### Instagram (Gold Tier)
- **Target:** Visual audience, younger demographic
- **Content:** Visual storytelling, infographics, carousel posts
- **Frequency:** 4-7 posts per week
- **Skill:** `post-to-social-media`

### Twitter/X (Gold Tier)
- **Target:** Tech community, real-time engagement
- **Content:** Quick insights, threads, industry commentary
- **Frequency:** 5-10 tweets per week
- **Skill:** `post-to-twitter`

## Content Workflow

1. **Content Creation:** AI generates platform-optimized posts
2. **Approval Request:** Files created in `/Pending_Approval`
3. **Human Review:** Move to `/Approved` to publish
4. **Publishing:** API helper scripts post to platforms
5. **Archiving:** Content saved in platform folders
6. **Analytics:** Engagement tracked for optimization

## File Naming Conventions

### Scheduled Posts
```
SCHEDULED_[PLATFORM]_[Topic]_[YYYY-MM-DD].md
```
Example: `SCHEDULED_TWITTER_AITips_2026-01-15.md`

### Published Posts
```
PUBLISHED_[PLATFORM]_[Topic]_[YYYY-MM-DD].md
```
Example: `PUBLISHED_FACEBOOK_Update_2026-01-12.md`

### Analytics
```
ANALYTICS_[PLATFORM]_[Month]_[Year].md
```
Example: `ANALYTICS_INSTAGRAM_January_2026.md`

## Integration with Other Systems

- **Dashboard:** Social metrics updated daily
- **CEO Briefing:** Weekly engagement summary included
- **Business Goals:** Social targets tracked and reported

## Automation Schedule

- **LinkedIn:** Post approval every Monday/Wednesday/Friday
- **Facebook:** Post approval every weekday
- **Instagram:** Post approval daily (7 days/week)
- **Twitter:** Real-time posting (approval as needed)

---

*Created: 2026-01-12*
*Branch: feat/gold-social-expansion*
*Version: 1.0*
