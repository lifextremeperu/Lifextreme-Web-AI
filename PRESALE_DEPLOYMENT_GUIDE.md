# Lifextreme Lifecoin Presale - Deployment Guide

## 🚀 Quick Start (Next 2 Weeks)

### Week 1: Setup & Testing

#### Day 1-2: Database Setup
1. **Run SQL Schema in Supabase**
   ```bash
   # Go to Supabase Dashboard → SQL Editor
   # Copy and paste content from: supabase_presale_schema.sql
   # Click "Run"
   ```

2. **Verify Tables Created**
   - `presale_investors`
   - `lifecoin_transactions`
   - `presale_stats`

#### Day 3-4: Deploy Pages
1. **Add presale.html to project**
   - Already created ✅
   - Test locally: Open in browser
   
2. **Update index.html**
   - Add link to presale in navigation
   - Add "Invest" CTA in hero section

3. **Deploy to Vercel**
   ```bash
   git add presale.html supabase_presale_schema.sql
   git commit -m "feat: add Lifecoin presale system"
   git push origin main
   vercel --prod
   ```

#### Day 5-7: Payment Integration

**For Yape (Manual Process)**:
1. Display QR code with your Yape number
2. User uploads screenshot
3. Admin verifies in Supabase
4. Manually update `payment_status` to 'verified'

**For PayPal (Automated)**:
1. Create PayPal Business account
2. Get API credentials
3. Integrate PayPal Checkout SDK
4. Set up webhook for confirmations

### Week 2: Launch & Marketing

#### Day 8-10: Soft Launch
1. **Email existing users** (50-100 people)
2. **Test payment flows** with real transactions
3. **Fix any bugs**

#### Day 11-14: Public Launch
1. **Social media campaign**
   - Instagram/Facebook ads
   - TikTok videos
   - LinkedIn posts

2. **Influencer outreach**
   - Adventure travel influencers
   - Startup community

3. **Create urgency**
   - "Only 100 spots"
   - Countdown timer
   - Show live investor count

---

## 📊 Expected Results

### Conservative Scenario
- 50 investors × $300 avg = **$15,000**

### Moderate Scenario
- 75 investors × $400 avg = **$30,000** ✅ TARGET

### Optimistic Scenario
- 100 investors × $500 avg = **$50,000**

---

## 🔧 Technical Implementation Status

### ✅ Completed
- [x] Presale landing page (`presale.html`)
- [x] Database schema (`supabase_presale_schema.sql`)
- [x] Investment packages (3 tiers)
- [x] Payment modal
- [x] Countdown timer
- [x] Stats tracking

### 🚧 In Progress
- [ ] Payment pages (Yape & PayPal)
- [ ] Investor dashboard
- [ ] Admin verification panel
- [ ] Email confirmations

### 📅 Next Phase (After Presale)
- [ ] Lifecoin redemption system
- [ ] Integration with booking flow
- [ ] Founder badge display
- [ ] Exclusive events calendar

---

## 💰 Use of Funds ($30K Target)

```
Immediate (Month 1-2):
$10,000 → Hire operations person
$5,000  → Marketing (ads, influencers)
$3,000  → Equipment inventory
$2,000  → Legal (contracts, compliance)
$10,000 → Buffer/Emergency fund

Month 3-6:
Use revenue + remaining funds to scale
Target: $20K/month in bookings
```

---

## 📞 Support & Questions

**Technical Issues**: Check Supabase logs
**Payment Questions**: Contact investors via email
**Legal**: Consult with lawyer before launch

---

## ⚠️ Important Reminders

1. **Legal Disclaimer**: Add to all pages
   > "Lifecoins are prepaid service credits, not securities. Non-refundable."

2. **Terms & Conditions**: Draft simple agreement
   - Non-refundable
   - Platform use only
   - No guaranteed returns
   - Subject to availability

3. **Customer Service**: Respond to investor questions within 24 hours

---

## 🎯 Success Metrics

Track weekly:
- Number of investors
- Total raised
- Average investment
- Conversion rate (visitors → investors)
- Payment method breakdown

---

Ready to launch! 🚀

Next immediate action: Deploy `presale.html` to production and share link for testing.
