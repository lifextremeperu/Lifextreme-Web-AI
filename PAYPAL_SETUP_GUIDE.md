# PayPal Integration Guide - Lifextreme Presale

## 🎯 Overview

This guide will help you set up PayPal payments for the Lifecoin presale system.

---

## 📋 Prerequisites

1. PayPal Business Account
2. Access to PayPal Developer Dashboard
3. Basic understanding of API keys

---

## 🚀 Step-by-Step Setup

### Step 1: Create PayPal Business Account

1. Go to [PayPal Business](https://www.paypal.com/business)
2. Click "Sign Up"
3. Choose "Business Account"
4. Complete registration with:
   - Business name: Lifextreme SAC
   - Business type: Corporation/LLC
   - Business email
   - Tax ID (RUC in Peru)

### Step 2: Access Developer Dashboard

1. Go to [PayPal Developer](https://developer.paypal.com/)
2. Log in with your PayPal Business account
3. Click "Dashboard" in top navigation

### Step 3: Create App Credentials

1. In Developer Dashboard, go to "My Apps & Credentials"
2. Click "Create App"
3. Fill in details:
   - **App Name**: Lifextreme Presale
   - **App Type**: Merchant
   - **Sandbox/Live**: Start with Sandbox for testing
4. Click "Create App"

### Step 4: Get API Credentials

After creating the app, you'll see:

```
Client ID: YOUR_CLIENT_ID_HERE
Secret: YOUR_SECRET_HERE
```

**IMPORTANT**: Keep these credentials secure!

### Step 5: Update payment-paypal.html

Open `payment-paypal.html` and replace the PayPal SDK line:

**Current (line 9):**
```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_PAYPAL_CLIENT_ID&currency=USD"></script>
```

**Replace with:**
```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_ACTUAL_CLIENT_ID&currency=USD"></script>
```

### Step 6: Test in Sandbox Mode

1. Use PayPal Sandbox accounts for testing
2. In Developer Dashboard, go to "Sandbox" → "Accounts"
3. You'll see test buyer and seller accounts
4. Use these credentials to test payments

**Test Buyer Account Example:**
- Email: sb-buyer@personal.example.com
- Password: (provided in dashboard)

### Step 7: Configure Webhooks (Optional but Recommended)

Webhooks notify your server when payments are completed.

1. In Developer Dashboard, go to "Webhooks"
2. Click "Add Webhook"
3. Enter webhook URL: `https://www.lifextreme.store/api/paypal-webhook`
4. Select events:
   - `PAYMENT.CAPTURE.COMPLETED`
   - `PAYMENT.CAPTURE.DENIED`
   - `PAYMENT.CAPTURE.REFUNDED`
5. Save webhook

### Step 8: Switch to Live Mode

Once testing is complete:

1. Go to "My Apps & Credentials"
2. Switch toggle from "Sandbox" to "Live"
3. Create new app or use existing
4. Get **Live** Client ID
5. Update `payment-paypal.html` with Live credentials

---

## 💳 Payment Flow

```
User selects package → Fills form → Chooses PayPal →
PayPal SDK loads → User logs into PayPal →
Payment processed → Webhook fired →
Data saved to Supabase → Confirmation page
```

---

## 🔧 Integration with Supabase

Update the `savePaymentToDatabase()` function in `payment-paypal.html`:

```javascript
async function savePaymentToDatabase(paypalDetails, packageName, amount) {
    // Import Supabase client
    const { createClient } = supabase;
    const supabaseUrl = 'YOUR_SUPABASE_URL';
    const supabaseKey = 'YOUR_SUPABASE_ANON_KEY';
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Calculate lifecoins based on package
    const lifecoinsMap = {
        'explorador': 2000,
        'aventurero': 10000,
        'pionero': 25000
    };

    const lifecoins = lifecoinsMap[packageName] || 10000;

    // Insert investor record
    const { data, error } = await supabase
        .from('presale_investors')
        .insert([{
            full_name: `${paypalDetails.payer.name.given_name} ${paypalDetails.payer.name.surname}`,
            email: paypalDetails.payer.email_address,
            phone: paypalDetails.payer.phone?.phone_number?.national_number || 'N/A',
            country: paypalDetails.payer.address?.country_code || 'US',
            package_name: packageName,
            amount_usd: parseFloat(amount),
            lifecoins_purchased: lifecoins,
            lifecoins_balance: lifecoins,
            payment_method: 'paypal',
            transaction_reference: paypalDetails.id,
            payment_status: 'verified', // PayPal is auto-verified
            founder_badge: packageName === 'pionero' ? 'platinum' : packageName === 'aventurero' ? 'gold' : 'bronze'
        }]);

    if (error) {
        console.error('Error saving to Supabase:', error);
    } else {
        console.log('Payment saved successfully:', data);
    }
}
```

---

## 🔒 Security Best Practices

### 1. Never Expose Secret Key
- Client ID: ✅ Safe to use in frontend
- Secret Key: ❌ NEVER put in frontend code
- Use Secret only in backend/serverless functions

### 2. Validate Payments Server-Side
Even though PayPal SDK confirms payments, always verify:

```javascript
// Backend verification (Node.js example)
const paypal = require('@paypal/checkout-server-sdk');

async function verifyPayment(orderId) {
    const request = new paypal.orders.OrdersGetRequest(orderId);
    const order = await client.execute(request);
    
    if (order.result.status === 'COMPLETED') {
        // Payment is legitimate
        return true;
    }
    return false;
}
```

### 3. Use Environment Variables

Create `.env` file:
```
PAYPAL_CLIENT_ID=your_client_id_here
PAYPAL_SECRET=your_secret_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

---

## 💰 Fee Structure

PayPal charges fees on transactions:

**Standard Rates (Peru):**
- Domestic: 4.4% + fixed fee
- International: 5.4% + fixed fee

**Example:**
- $500 payment
- Fee: ~$22 (4.4%)
- You receive: ~$478

**Factor this into your pricing!**

---

## 🧪 Testing Checklist

- [ ] Sandbox payment completes successfully
- [ ] Confirmation page displays correct info
- [ ] Data saves to Supabase correctly
- [ ] Email confirmation sent (if implemented)
- [ ] Error handling works (declined cards, etc.)
- [ ] Mobile responsive
- [ ] Works on different browsers

---

## 🚨 Common Issues & Solutions

### Issue 1: "Client ID not found"
**Solution**: Make sure you copied the entire Client ID correctly

### Issue 2: Payment button doesn't appear
**Solution**: Check browser console for errors. Ensure PayPal SDK loaded.

### Issue 3: Payment succeeds but data not saved
**Solution**: Check Supabase RLS policies. Ensure `presale_investors` table allows inserts.

### Issue 4: Webhook not firing
**Solution**: 
- Verify webhook URL is publicly accessible
- Check webhook signature validation
- Review PayPal webhook logs in dashboard

---

## 📊 Monitoring Payments

### PayPal Dashboard
1. Log into PayPal Business account
2. Go to "Activity"
3. Filter by date range
4. Export reports for accounting

### Supabase Dashboard
1. Go to Table Editor
2. View `presale_investors` table
3. Filter by `payment_method = 'paypal'`
4. Check `payment_status` column

---

## 🔄 Refund Process

If you need to refund a payment:

1. Go to PayPal Business Dashboard
2. Find transaction in Activity
3. Click "Refund"
4. Update Supabase:
```sql
UPDATE presale_investors
SET payment_status = 'refunded',
    lifecoins_balance = 0
WHERE transaction_reference = 'PAYPAL_TRANSACTION_ID';
```

---

## 📧 Email Notifications (Optional)

Set up automatic emails when payment completes:

```javascript
async function sendConfirmationEmail(investorEmail, packageName, lifecoins) {
    // Use SendGrid, Mailgun, or Supabase Edge Functions
    const emailData = {
        to: investorEmail,
        subject: '¡Bienvenido al Club de Fundadores de Lifextreme!',
        html: `
            <h1>¡Gracias por tu inversión!</h1>
            <p>Has recibido ${lifecoins} Lifecoins</p>
            <p>Paquete: ${packageName}</p>
            <p>Beneficios activados:</p>
            <ul>
                <li>50% descuento vitalicio</li>
                <li>Badge de fundador</li>
                <li>Acceso prioritario</li>
            </ul>
        `
    };
    
    // Send email via your preferred service
}
```

---

## 🎯 Next Steps

1. ✅ Create PayPal Business account
2. ✅ Get API credentials
3. ✅ Update `payment-paypal.html` with Client ID
4. ✅ Test in Sandbox mode
5. ✅ Integrate with Supabase
6. ✅ Set up webhooks
7. ✅ Switch to Live mode
8. ✅ Monitor first real payments

---

## 📞 Support

**PayPal Support:**
- Phone: 1-888-221-1161
- Help Center: https://www.paypal.com/help

**Technical Issues:**
- PayPal Developer Forums
- Stack Overflow (tag: paypal)

---

## 🔗 Useful Links

- [PayPal Developer Docs](https://developer.paypal.com/docs/)
- [PayPal SDK Reference](https://developer.paypal.com/sdk/js/)
- [Webhook Events](https://developer.paypal.com/api/rest/webhooks/)
- [Testing Guide](https://developer.paypal.com/tools/sandbox/)

---

**Ready to accept payments! 🚀**
