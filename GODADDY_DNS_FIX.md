# GoDaddy DNS Fix for injoybeauty.ca

## 🔴 The Problem I Found

Looking at your GoDaddy DNS records:

**❌ WRONG**: 5 A records for `@` pointing to old IPs:
- 185.199.108.153
- 185.199.109.153
- 185.199.110.153
- 185.199.111.153
- 216.24.57.1

**✅ CORRECT**: CNAME for `www` pointing to `injoybeauty.onrender.com`

## ⚠️ Important Note About GoDaddy

GoDaddy **does NOT support CNAME records on the root domain** (`@`). You must use A records instead.

## ✅ Step-by-Step Fix

### Step 1: Confirm the Render IP Address

✅ **You already have the Render IP**: `216.24.57.1`

I can see this IP is already in one of your A records, but you have 4 other A records pointing to wrong IPs. We need to remove those and keep only the Render IP.

### Step 2: Delete Wrong A Records in GoDaddy

1. **In GoDaddy DNS Management** (where you are now):
2. **Delete ONLY the 4 WRONG A records** for `@`:
   - Click "Delete" (or trash icon) for each of these:
     - `Type: A, Name: @, Data: 185.199.108.153` ❌ DELETE
     - `Type: A, Name: @, Data: 185.199.109.153` ❌ DELETE
     - `Type: A, Name: @, Data: 185.199.110.153` ❌ DELETE
     - `Type: A, Name: @, Data: 185.199.111.153` ❌ DELETE
3. **KEEP this one** (it's correct):
   - `Type: A, Name: @, Data: 216.24.57.1` ✅ KEEP THIS ONE
4. **Confirm deletion** for each wrong record

### Step 3: Verify the Correct A Record

After deleting the 4 wrong A records, you should have:
- ✅ **ONE A record** for `@`:
   - `Type: A, Name: @, Data: 216.24.57.1`
   - **TTL**: `1 Hour` (or whatever it's set to)

**If the A record with 216.24.57.1 was accidentally deleted**, add it back:
1. **Click "Add" or "Add Record"** button
2. **Create A record**:
   - **Type**: `A`
   - **Name**: `@` (or leave blank - GoDaddy will use `@`)
   - **Data/Value**: `216.24.57.1`
   - **TTL**: `1 Hour` (or default)
3. **Click "Save"**

**Important**: You should have ONLY ONE A record for `@` pointing to `216.24.57.1`

### Step 4: Verify www CNAME (Should Already Be Correct)

Your `www` CNAME is already correct:
- ✅ `Type: CNAME, Name: www, Data: injoybeauty.onrender.com.`

**Don't change this!** It's already pointing to Render correctly.

### Step 5: Save and Wait

1. **Save all changes** in GoDaddy
2. **Wait for DNS propagation**:
   - Check at: https://dnschecker.org
   - Enter: `injoybeauty.ca`
   - Select: `A` record
   - Should show your new Render IP address
   - Usually takes 1-2 hours (can take up to 48 hours)

3. **Wait for SSL certificate**:
   - After DNS propagates, Render auto-provisions SSL
   - Takes 5-30 minutes
   - Check status in Render dashboard → Custom Domains → SSL Certificate
   - Wait until shows "Active"

### Step 6: Test

Once DNS has propagated and SSL is Active:
- Try: `https://injoybeauty.ca`
- Should load without SSL errors!

## 🔍 Alternative: If Render Doesn't Provide IP

If Render only shows CNAME instructions (not A record IPs):

### Option A: Use ALIAS/ANAME Record (If GoDaddy Supports It)
- Some registrars support ALIAS/ANAME records on root domain
- Check if GoDaddy has this option
- Use ALIAS pointing to `injoybeauty.onrender.com`

### Option B: Contact Render Support
- Ask them for the A record IP address(es) for your service
- They should be able to provide this

### Option C: Use DNS Lookup Tools
- Use `dig injoybeauty.onrender.com` or online tools
- Find the IP address that `injoybeauty.onrender.com` resolves to
- Use that IP for your A record

**However**, this might not work if Render uses dynamic IPs or load balancers. **Best to get the official IP from Render.**

## 📋 Quick Checklist

- [x] Got IP address from Render: `216.24.57.1` ✅
- [ ] Deleted 4 wrong A records (185.199.x.x IPs) in GoDaddy
- [ ] Verified only ONE A record exists: `@` → `216.24.57.1`
- [ ] Verified `www` CNAME is still correct (it is!)
- [ ] Saved changes in GoDaddy
- [ ] Checked DNS propagation at dnschecker.org
- [ ] Waited for SSL certificate to become "Active" in Render
- [ ] Tested `https://injoybeauty.ca`

## ⚠️ Important Notes

1. **Don't delete the NS records** - those are system-managed
2. **Don't delete the SOA record** - that's system-managed
3. **Keep the www CNAME** - it's already correct
4. **Root domain must use A records** - GoDaddy doesn't support CNAME on `@`
5. **DNS changes can take up to 48 hours** to fully propagate globally

## 🎯 Expected Result

After fixing:
- `https://injoybeauty.ca` loads correctly (root domain)
- `https://www.injoybeauty.ca` loads correctly (www subdomain - already working)
- Both show green padlock (secure connection)
- No SSL errors

---

**Need the Render IP?** Check Render dashboard → Your Service → Settings → Custom Domains → `injoybeauty.ca` → Look for A record instructions.
