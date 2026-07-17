import pandas as pd
import random

random.seed(42)

names = ["Alex", "Sarah", "Mark", "Priya", "Jordan", "Chris", "Emily", "Raj", "Taylor", "Sam",
         "Jordan", "Morgan", "Casey", "Riya", "David", "Nina", "Omar", "Lena", "Jake", "Zara"]
companies = ["Microsoft", "the IT department", "HR", "Finance", "the payroll team", "our vendor partner",
             "Google", "the security team", "our delivery partner", "the benefits team", "Amazon",
             "the accounts team", "our bank", "the university portal", "the internship program"]
amounts = ["$2.99", "$4.50", "$12.00", "a small fee", "$25", "$8.75", "a processing fee", "$50"]
links = ["forms.gle/verifyNow2026", "secure-update-portal.com", "account-check-fast.net",
         "confirm-details-now.info", "verify-quick.com/action", "portal-secure-access.net",
         "claim-now-fast.com", "reset-account-secure.info"]
deadlines = ["within 24 hours", "by end of day", "before Friday", "within 48 hours",
             "immediately", "by tomorrow", "before your next payment", "within 3 days"]

# (intent, formal_template, casual_template, corporate_template)
intents = [
    ("payroll", 
     "Dear Employee, please update your direct deposit information via the secure portal below {deadline}. {link}",
     "hey {name} here, finance changed the payroll system again, can u just drop ur account details here {deadline_lower} lol: {link}",
     "Hi team, as part of this month's payroll reconciliation, please confirm your banking details through the linked form {deadline_lower}. {link}"),
    ("invoice",
     "Dear Sir/Madam, your recent invoice could not be processed due to incomplete banking information. Please resubmit your details {deadline} via: {link}",
     "yo the invoice bounced back, can u just resend ur bank details here so i can push the payment thru {deadline_lower}: {link}",
     "Following up on last week's invoice, our accounts team flagged a mismatch. Could you confirm the correct details {deadline_lower} via this form? {link}"),
    ("it_security",
     "Dear Team Member, {company} has detected a policy violation on your workstation. Please verify your credentials {deadline} to avoid suspension: {link}",
     "hey its {name} from IT, we're migrating everyone to the new system, just need u to confirm ur login here {deadline_lower} so we dont lock u out: {link}",
     "As part of our transition to new infrastructure, please verify your account access {deadline_lower} using the link below. {link}"),
    ("internship",
     "Dear Applicant, congratulations on being shortlisted for our Internship Program! Please complete the enrollment form and submit the registration fee {deadline}: {link}",
     "heyy saw ur profile, we're offering a paid virtual internship, just fill this form to lock in ur spot {deadline_lower}: {link}",
     "We are pleased to inform you that you have been selected for our Skill Development Program with {company}. Kindly complete registration {deadline_lower}: {link}"),
    ("delivery",
     "Dear Customer, our courier attempted delivery but could not access your address. Please settle the redelivery fee of {amount} {deadline}: {link}",
     "ur package couldnt be delivered today, pls confirm ur address and pay {amount} here {deadline_lower}: {link}",
     "This is {company} delivery services. Your package is on hold due to an unpaid fee of {amount}. Please settle this {deadline_lower}: {link}"),
    ("ceo_wire",
     "Dear Finance Team, per the CEO's request during today's call, please process the attached wire transfer to our new supplier {deadline}. Confirm once completed.",
     "hey its me, stuck in a meeting rn, can u send {amount} to this account for me real quick, will explain later, kinda urgent, need it {deadline_lower}",
     "Hi, this is {name} from the CEO's office. He asked me to have you process an urgent wire transfer to a new vendor account {deadline_lower}. Details attached."),
    ("account_signin",
     "Dear User, unusual sign-in activity has been detected on your account. Please confirm your identity {deadline} to avoid a lock: {link}",
     "hey saw a login alert from ur account just now, might wanna check this real quick {deadline_lower}: {link}",
     "We noticed a new sign-in to your account from an unrecognized device {deadline_lower}. If this wasn't you, please secure your account: {link}"),
    ("benefits",
     "Dear Employee, as part of this year's benefits renewal, please complete your enrollment form {deadline}. This is mandatory for all employees: {link}",
     "hey its {name} from hr, quick one, benefits form needs updating {deadline_lower}, just fill this real quick: {link}",
     "As part of {company}'s annual review, please complete your enrollment {deadline_lower} to continue coverage. {link}"),
    ("gift_cards",
     "Dear Colleague, I'm currently traveling and unable to make calls. Could you purchase gift cards for a client gesture {deadline} and send me the codes? I'll reimburse you.",
     "heyy quick favor, can u buy a few gift cards for a client meeting today, ill pay u back later, need it {deadline_lower}, send the codes when u get them",
     "Hi {name}, per our earlier conversation, please pick up gift cards for the client appreciation event {deadline_lower} and share the codes for the file."),
    ("bank_fraud",
     "Dear Customer, {company} has flagged suspicious activity on your account. Please verify your card details {deadline} to prevent unauthorized charges: {link}",
     "hey ur card got flagged for some sus activity, can u just confirm the card number here {deadline_lower} so we can sort it: {link}",
     "This is {company}'s fraud prevention team. Please verify your account details {deadline_lower} to avoid a temporary hold: {link}"),
    ("subscription",
     "Dear Customer, your subscription payment failed to process. To avoid service interruption, please update your billing information {deadline}: {link}",
     "hii ur subscription payment didnt go through, can u update ur card details here {deadline_lower} so it doesnt get cancelled: {link}",
     "We were unable to process your latest subscription payment. Please update your billing details {deadline_lower} to avoid interruption: {link}"),
    ("password_reset",
     "Dear Team, following our recent security audit, all employees are required to reset their passwords {deadline} to remain compliant: {link}",
     "hey IT here, doing a quick password reset for everyone {deadline_lower}, just click this and set a new one: {link}",
     "As part of our ongoing security review, please reset your password {deadline_lower} using the secure link below: {link}"),
    ("refund",
     "Dear Valued Customer, you have received a refund of {amount}. Please confirm your bank details {deadline} to receive it: {link}",
     "heyy u got a refund pending from ur last order, just confirm ur account info here {deadline_lower}: {link}",
     "We are processing a refund of {amount} to your account. Please confirm your details {deadline_lower} via the secure form: {link}"),
    ("university",
     "Dear Student, your university account has been flagged for unusual activity. Please verify your login credentials {deadline} to avoid suspension: {link}",
     "hey saw some weird activity on ur student account, might wanna verify ur login {deadline_lower} before it gets locked: {link}",
     "The registrar's office has flagged your account for review. Please verify your credentials {deadline_lower}: {link}"),
    ("job_offer",
     "Dear Candidate, we were impressed with your profile and would like to move forward. Please complete onboarding and submit ID verification {deadline}: {link}",
     "hey its been a while! saw ur resume online, we have an opening that matches perfectly, just fill this quick form {deadline_lower}: {link}",
     "Thank you for your interest in the position. Please complete the enrollment form {deadline_lower} to confirm your offer: {link}"),
]

def fill(template, name, company, amount, link, deadline):
    return template.format(name=name, company=company, amount=amount, link=link,
                            deadline=deadline, deadline_lower=deadline.lower())

phishing_rows = []
for intent, formal_t, casual_t, corp_t in intents:
    for _ in range(12):  # 12 variations per intent per tone = 12*3*15 = 540 phishing rows
        name = random.choice(names)
        company = random.choice(companies)
        amount = random.choice(amounts)
        link = random.choice(links)
        deadline = random.choice(deadlines)
        phishing_rows.append(fill(formal_t, name, company, amount, link, deadline))
        phishing_rows.append(fill(casual_t, name, company, amount, link, deadline))
        phishing_rows.append(fill(corp_t, name, company, amount, link, deadline))

# Legitimate email templates (casual + formal + corporate, no malicious ask)
legit_templates = [
    "Dear Team, please find attached the {topic} summary for review ahead of {day}'s meeting. Let me know if you have questions.",
    "hey just wrapped up the {topic} call, they want us to push the deadline by a week, ill send the updated timeline tmrw",
    "Hi all, reminder that the office will be closed next {day} for the holiday. Please plan your {topic} accordingly.",
    "hey can u send over the notes from todays {topic} meeting, missed the first few mins",
    "Dear Colleagues, please see below for the updated {topic} timeline following yesterday's discussion.",
    "yo {topic} at the usual spot today? thinking around 1?",
    "Hi team, reminder to submit your {topic} by end of day {day} for this cycle.",
    "hey hows the {topic} coming along, need it by {day} if possible",
    "Dear All, the {topic} meeting has been rescheduled to next {day} at 10am. Calendar invite to follow.",
    "hii can u forward me the {topic} slides from last week when u get a sec",
    "Hi, thanks for your patience while we resolved the {topic} delay. Everything should be sorted by {day}.",
    "hey good catch on that {topic} issue, fixed it and pushed the update, lmk if u see anything else weird",
    "Dear Team, attached are the {topic} notes from today's sync. Action items are highlighted for each of you.",
    "quick q, are we still doing the {topic} review on {day} or did that move",
    "Hi everyone, welcome to the team! Reach out if you have questions about {topic} as you settle in this week.",
    "Dear {name}, thanks for your work on the {topic} project this quarter, really appreciate the effort.",
    "hey {name}, can u loop me in on the {topic} thread, think i got left off by accident",
    "Hi team, just confirming we're on track for the {topic} deliverable by {day}. Let me know if there are blockers.",
    "Dear Colleagues, sharing the {topic} report a bit early this week since {day} is a holiday.",
    "hey {name} out sick today, can someone cover the {topic} standup",
]
topics = ["budget", "sprint", "client", "onboarding", "quarterly", "marketing", "product",
          "engineering", "design", "hiring", "roadmap", "vendor", "audit", "training", "logistics"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "next week"]

legit_rows = []
for _ in range(160):  # 160 legit rows
    t = random.choice(legit_templates)
    legit_rows.append(t.format(topic=random.choice(topics), day=random.choice(days), name=random.choice(names)))

# Deduplicate just in case any exact repeats slipped through
phishing_rows = list(dict.fromkeys(phishing_rows))
legit_rows = list(dict.fromkeys(legit_rows))

df = pd.DataFrame(
    {"text": phishing_rows + legit_rows,
     "label": [1] * len(phishing_rows) + [0] * len(legit_rows)}
)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("adversarial_examples.csv", index=False)
print(f"Total rows: {len(df)}")
print(f"Phishing: {sum(df['label']==1)}, Legit: {sum(df['label']==0)}")