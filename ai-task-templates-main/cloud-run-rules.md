Title: Cloud Run Hackathon

URL Source: https://run.devpost.com/rules

Markdown Content:
#### Cloud Run Hackathon Official Eligibility and Rules

NO PURCHASE NECESSARY TO ENTER OR WIN. VOID WHERE PROHIBITED. CONTEST IS OPEN TO EVERYONE EXCEPT FOR RESIDENTS OF ITALY, QUEBEC, CRIMEA, CUBA, IRAN, SYRIA, NORTH KOREA, SUDAN, BELARUS, RUSSIA, AND OR AS LISTED AS INELIGIBLE IN THE ELIGIBILITY SECTION BELOW.

ENTRY IN THIS CONTEST CONSTITUTES YOUR ACCEPTANCE OF THESE OFFICIAL RULES.

The Cloud Run Hackathon (the “Contest”) is a skill contest where Google will share specific challenges set forth in these Rules as well as in the Devpost page for this Contest, and participants must develop solutions to one of the challenges. The solution that you develop and submit will be evaluated by judges, who will choose the winner(s) in accordance with these Official Rules. The prize(s) will be awarded to the participant(s) with the highest score for the judging criteria. See below for the complete details.

**1. BINDING AGREEMENT:**

In order to enter the Contest, you must agree to these Official Rules (“Rules”). Therefore, please read these Rules prior to entry to ensure you understand and agree. You agree that submission of an entry in the Contest constitutes agreement to these Rules. You may not submit an entry to the Contest and are not eligible to receive the prizes described in these Rules unless you agree to these Rules. These Rules form a binding legal agreement between you and Google with respect to the Contest.

**2. SPONSOR:**

The Contest is sponsored by Google LLC (“Google” or “Sponsor”), a Delaware corporation located at 1600 Amphitheater Parkway, Mountain View, CA, 94043, USA. The Contest will be administered by Devpost, Inc. (“Devpost” or “Administrator”) located at 222 Broadway, Floor 19, New York, NY 10038.

**3. ELIGIBILITY:**

To be eligible to enter the Contest, you must: (1) be above the age of majority in the country, state, province or jurisdiction of residence (or at least twenty years old in Taiwan) at the time of entry; (2) not be a resident of Italy, Quebec, Crimea, Cuba, Iran, Syria, North Korea, Sudan, Belarus, Russia and any other country designated by the United States Treasury's Office of Foreign Assets Control; (3) not be a person or entity under U.S. export controls or sanctions; and (4) have access to the Internet as of October 6, 2025. Contest is void in Italy, Quebec, Crimea, Cuba, Iran, Syria, North Korea, Sudan and where prohibited by law. Employees, interns, contractors, and official office-holders of Google, Devpost, or any organizations involved with the design, production, paid promotion, execution, or distribution of the Contest, and their parent companies, subsidiaries, affiliates, and their respective directors, officers, employees, advertising and promotion agencies, representatives, and agents or their immediate family or members of their household (“Contest Entities”), and members of the Contest Entities’ and their immediate families (parents, siblings, children, spouses, and life partners of each, regardless of where they live) and members of the households (whether related or not) of such employees, officers and directors are ineligible to participate in this Contest. Sponsor reserves the right to verify eligibility and to adjudicate on any dispute at any time. Persons who are (1) residents of US embargoed countries, (2) ordinarily resident in US embargoed countries, or (3) otherwise prohibited by applicable export controls and sanctions programs may not participate in this contest. In addition, individuals or organizations that are employed by a government agency, or any other individual or organization whose participation in the Contest would create, in the sole discretion of the Sponsor and/or Administrator, a real or apparent conflict of interest are ineligible to participate in this Contest.

If you are entering as part of a company or on behalf of your employer, these rules are binding on you, individually, and/or your employer. If you are acting within the scope of your employment, as an employee, contractor, or agent of another party, you warrant that such party has full knowledge of your actions and has consented thereto, including your potential receipt of a prize. You further warrant that your actions do not violate your employer’s or company’s policies and procedures.

**4. CONTEST PERIOD:**

The Contest begins at **9:00 A.M. Pacific Time** (PT) Zone in the United States on **October 6, 2025** and ends at **5:00 P.M. PT** on **November 10, 2025** (“Contest Period”). ENTRANTS ARE RESPONSIBLE FOR DETERMINING THE CORRESPONDING TIME ZONE IN THEIR RESPECTIVE JURISDICTIONS.

**5. HOW TO ENTER:**

NO PURCHASE NECESSARY TO ENTER OR WIN. To enter the Contest, visit the Contest website located at run.devpost.com (“Contest Site”) during the Contest Period, find the challenges provided by Google on the Devpost site, which challenges are also set forth in these Rules and develop a solution for the challenge. To access the challenge and submit the solution, follow the steps below

Obtain access to the submission portal. You must have a Devpost account to register for the Contest as they will administer the Contest. If you do not have a Devpost account already, you can sign up for a Devpost account at no cost from run.devpost.com.

Obtain access to Google Cloud developer tools. Access to Google Cloud may be obtained by (1) signing up for a no cost trial at [https://cloud.google.com/free](https://cloud.google.com/free) or (2) using an existing Google Cloud account for which you may request $100 in Google Cloud credits by completing this form by **November 7th at 12:00 pm PT**:

[https://forms.gle/YKSxTsJffi9Wow4a8](https://forms.gle/YKSxTsJffi9Wow4a8). The credit should be approved within **72 business hours** of completing the form. Provision of credits to you is not guaranteed and at Google’s discretion. You are responsible for any and all fees accrued from use of Google Cloud developer tools if your use of these tools in connection with this Contest exceeds the $100 credit amount. When submitting information to request a credit, your data will be processed in accordance with the Google Privacy Policy at https://policies.google.com/privacy. Use of Google Cloud Google Cloud developer tools will be subject to the license agreement applicable to the use of those services. Entry in the Contest constitutes consent for the Sponsor and Devpost to collect and maintain an entrant’s personal information for the purpose of operating and publicizing the Contest.

Create a project in line with the Project Requirements below. Use Google Cloud service(s) to tackle a challenge using the information provided in the repository to complete a Project that fits into that requirements set forth in the Project Requirements section below.

Submit Your project to the Contest Site. Make sure to complete and enter all of the required fields on the “Enter a Submission” or similar worded page of the Contest Site (each a “Submission”) during the Contest Period.

**6. SUBMISSION REQUIREMENTS:**

**A. CHOOSE A CHALLENGE**

Build your solutions within one of the following categories:

*   **AI Studio Category**: Take an idea and make it into code. Use Google AI Studio to vibe code your idea and deploy the app to Cloud Run. 
    *   Details: Your project could be a web service, a data processing pipeline, a backend for a mobile app, or any other creative serverless solution. Must be coded with Google AI Studio and deploy to Cloud Run using the applet function.

*   **AI Agents Category**: Build an AI agent application and deploy it to Cloud Run 
    *   Details: Build an agent-based application using Google ADK. Application can be solving a real-world problem, improving a process to creating a custom research assistant tool.

*   **GPU Category**: Harness the power of GPUs on Cloud Run to run AI and ML models. 
    *   Details: Project must deploy and run an open-source model (like Gemma) on a Cloud Run service configured with a GPU

**Key technologies to be leveraged include:**

**General Requirements (all categories)**

1.   Across all categories, your project **must** be deployed on Cloud Run. Feel free to take advantage one (or more) of the three resource types in Cloud Run:

*       *   **Service** Responds to HTTP requests sent to a unique and stable endpoint, using stateless, ephemeral instances that autoscale based on a variety of key metrics, also responds to events and functions.
    *   **Job** Handles non-request-based parallelizable tasks that are executed manually, or on a schedule, and run to completion.
    *   **Worker pool** Handles non-request-based workloads such as pull-based workloads, for example, Kafka consumers, Pub/Sub pull queues, or RabbitMQ consumers.

**Allowed Technologies (Optional):**

While Cloud Run is foundational, you are **allowed and encouraged** to enhance your solutions by integrating with other relevant technologies and frameworks within the Google Cloud ecosystem.

*   **Foundation Models**: We highly encourage and will reward the use of Gemini models and other Google models like Imagen and Veo. You can explore and integrate other foundation models like Anthropic (Claude 3.5, 3.7), but you should focus on the use of Gemini models where possible.
*   **Cloud Run MCP server**
*   **CLI based AI Assistance**: Use Gemini CLI to help with developing your application. You can also explore other tools like Anthropic Claude Code but we encourage you to use Gemini CLI where possible.
*   **GCP Services:** We encourage you to to integrate with other GCP services for storing and retrieving data for your Run application: 
    *   **Cloud Storage** blob store
    *   **BigQuery data** warehousing and analysis
    *   **Firestore** for NoSQL
    *   And more!

*   **IoT & Mobile devices**: You are not constrained to only use web services, your Run application can power other use cases such as IoT or Mobile devices.

**B. ESSENTIAL COMPONENTS OF SUBMISSION**. The Submission must conform to the following requirements (hereinafter, “Requirements”):

**Project Team:** You may submit your Project as an individual, a team, or on behalf of an organization. A Team must consist of only Eligible Individuals, have all team members added as members of the Project on Devpost. If a team or organization is entering the Submission, one individual must be appointed and authorized (the “Representative”) to represent, act, and enter the Submission, on the team’s behalf.

**Functionality**: The Project must use Cloud Run as the foundation of your project.The Project must be capable of being successfully installed and run consistently on the platform for which it is intended, and must function as depicted in the video and/or expressed in the text description that you submit with the Project.

**New Projects Only**: Projects must be newly created by the entrant during the Contest Period. The Project must be your original creation not a modification or extension of Your or anyone else’s existing work.

**Third-Party Integrations**: If a Project integrates any third-party SDK, APIs, data and/or any information belonging to a third party, Entrants must be authorized to use these third-party tools and information in accordance with any terms and conditions or licensing requirements of the tool. If using third-party integrations/content/etc;, you must indicate it in your submission description.

**Testing:** Access must be provided to an Entrant’s working Project (if available) for judging and testing by providing a link to a website, functioning demo, or a test build. If Entrant’s website is private, Entrant must include login credentials in its testing instructions. The Entrant must make the Project available free of charge and without any restriction, for testing, evaluation and use by the Sponsor, Administrator and Judges until the Judging Period ends. Judges are not required to test the Project and may choose to judge based solely on the text description, images, and video provided in the Submission.

If the Project includes software that runs on proprietary or third party hardware that is not widely available to the public, including software running on devices or wearable technology other than smartphones, tablets, or desktop computers, the Sponsor and/or Administrator reserve the right, at their sole discretion, to require the Entrant to provide physical access to the Project hardware upon request.

#### **What to Submit**:

*   Include a **Project** built with the required developer tools and meets the above Project Requirements.
*   Select one **category** which represents your project (if applicable, or your organization (if submitting as an organization). Please note that Submissions will be associated by the category selected. The Sponsor and Administrator reserve the right to reassign a Submission from one category to another if applicable.
*   Include a **URL to the hosted Project**(if available) for judging and testing, such as web UI, Chrome Extension, mobile app, etc. A hosted project is highly encouraged.
*   Include a **comprehensive text description** that should include a summary of the Project’s features and functionality, **technologies used**, information about any other data sources used, and your findings and learnings as you worked through the project. Written parts of entries must be in English to be eligible. The Project must, at a minimum, support English language use.
*   Include a URL to your **public code repository** to show how your project was built. The code repository must be public to allow access for judging and testing.
*   Include an **Architecture Diagram** showing which technologies were used and how they interact with one another.
*   Include a **demonstration video** of your Project. The video portion of the Project: 
    *   Should include footage that shows the Project functioning on the platform(s) for which it was built.
    *   It should not be longer than **3 minutes**. If it is longer than 3 minutes, only the first 3 minutes will be evaluated.
    *   It must conform to the technical requirements set forth on the Contest site, including that the Submission must be uploaded to and made publicly visible on YouTube or Vimeo, and a link to the video must be provided on the Submission form on the Contest Site.
    *   It must be in English or include **English subtitles**.

*   [EDITED 10/17 to clarify] If entering the AI Studio Category, must provide your **prompts in AI Studio**by sharing the link to your app using the Share App functionality in AI Studio
*   No parts of the submission can be derogatory, offensive, threatening, defamatory, disparaging, libelous or contain any content that is inappropriate, indecent, sexual, profane, indecent, tortuous, slanderous, discriminatory in any way, or that promotes hatred or harm against any group or person, or otherwise does not comply with the theme and spirit of the Contest.
*   No part of that submission contains content, material or any element that is unlawful, or otherwise in violation of or contrary to all applicable federal, state, or local laws and regulations in any country, state or applicable territory where you created the video and in the United States.
*   The Submission must not contain any content, material or element that displays any third party advertising, slogan, logo, trademark or otherwise indicates a sponsorship or endorsement by a third party, commercial entity or that is not within the spirit of the Contest, as determined by Sponsor, in its sole discretion.
*   It cannot contain any content, element, or material that violates a third party’s publicity, privacy or intellectual property rights.

*   **Optional Additional Google Cloud Contributions**: Submitting the following optional components will positively impact the score the submission receives from the Judges. 
    *   **The use of a Google AI model**: Including but not limited to models like Gemini, Gemma, Veo, etc.
    *   **Cloud Run**: The points will be added if the project runs multiple services, need a front & back end. (leveraging more Cloud Run services).

*   **Optional Developer Contributions**: Submitting the following optional components will positively impact the score the submission receives from the Judges. 
    *   **Publishing a piece of content (blog, podcast, video)**: Covering how the project was built using **Cloud Run** on any public platform (e.g., medium.com, dev.to, Youtube, etc.). The content must be public (not unlisted). You must include language that says you created the piece of content for the purposes of entering this hackathon.
    *   **Publishing a social media post**: Highlighting or promoting your project on social media post on X, LinkedIn, Instagram, or Facebook. For any social media posts on platforms such as X or LinkedIn, include the hashtag **#CloudRunHackathon**.

**7. SUBMISSION MODIFICATIONS**: Prior to the end of the Contest Period, you may save draft versions of your submission on Devpost to your portfolio before submitting the Submission materials to the Contest for evaluation. Once the Contest Period has ended, you may not make any changes or alterations to your Submission, but you may continue to update the Project in your Devpost portfolio. After the Contest Period, fully at their discretion, the Sponsor and Devpost may permit you to modify part of your Submission after the Contest Period for the purpose of adding, removing or replacing material that potentially infringes a third party mark or right, discloses personally identifiable information, or is otherwise inappropriate. The modified Submission must remain substantively the same as the original Submission with the only modification being what the Sponsor and Devpost permits.

**8. JUDGING:** On or about the period between **November 10, 2025** through **December 5, 2025**, (“Judging Period”) the Submissions will be evaluated by the Judges in the following Stages. Eligible submissions will be evaluated by a panel of judges selected by the Sponsor (the “Judges”). Judges may be employees of the sponsor or third parties, may or may not be listed individually on the Hackathon Website, and may change before or during the Judging Period. Judging may take place in one or more rounds with one or more panels of Judges, at the discretion of the sponsor.

The Submissions will be evaluated by the Judges in the following Stages:

*   **Stage One**: The first stage will determine via pass/fail whether the Submission meets a baseline level of viability, in that the Submission includes all Submission requirements, reasonably addresses a Challenge, and reasonably applies the requirements.

*   **Stage Two**: All Submissions that pass Stage One will be evaluated in Stage Two by the Judges based on the following weighted criteria, and according to the sole and absolute discretion of the Judges. Each Submission will receive a score from 1 to 5 per criterion and those criterion scores will be averaged per Submission.
*       *   **Technical Implementation (40%)**: Technical Implementation (40%): Is it technically well executed? Is the code clean, efficient, and well-documented? Does it utilize the core concepts of Cloud Run? Is the app intuitive and user-friendly? Is it a proof-of-concept or can it be scaled to production use with error handling?
    *   **Demo and Presentation (40%)**: Is the problem clearly defined, and is the solution effectively presented through a demo and documentation? Have they explained how they used Cloud Run and relevant tools? Have they included documentation or an architectural diagram?
    *   **Innovation and Creativity (20%)**: How novel and original is the idea? Does it address a significant problem or create a unique solution? How significant is the problem the project addresses, and does it efficiently solve it?

*   **Stage Three**: The Submissions that pass Stage One and Two will be evaluated based on **Bonus Contributions**: 
    *   **Optional Additional Google Cloud Contributions**: Those who submit the following will receive bonus points that contribute to their overall score: 
        *   **The use of a Google AI model**: Including but not limited to models like Gemini, Gemma, Veo, etc., maximum of 0.4 points will be added
        *   **Cloud Run**: The points will be added if the project runs multiple services, need a front & back end. (leveraging more Cloud Run services), a maximum of 0.4 points will be added

    *   **Optional Developer Contributions:** Submitting the following optional components will positively impact the score the submission receives from the Judges. 
        *   **Publishing a piece of content (blog, podcast, video)**: Covering how the project was built using **Cloud Run** on any public platform (e.g., medium.com, dev.to, Youtube, etc.). The content must be public (not unlisted). You must include language that says you created the piece of content for the purposes of entering this hackathon, a maximum of 0.4 points will be added
        *   **Publishing a social media post**: Highlighting or promoting your project on social media post on X, LinkedIn, Instagram, or Facebook. For any social media posts on platforms such as X or LinkedIn, include the hashtag**#CloudRunHackathon**. A maximum of 0.4 points will be added

**Each Submission will receive a Final score from 1 to 6.6, with the highest possible Final score being 6.6.**

The highest-scoring Submission for each category will be selected as the potential winner(s). The highest-scoring Submission across all categories will win the Grand Prize. Ties will be broken by comparing scores on each criterion in the order listed, and if a tie remains, judges will vote. If a potential winner is disqualified, the Submission with the next highest score will become the potential winner. Determinations of judges are final and binding.

The award of a prize to a potential winner is subject to verification of the identity, qualifications and role of the potential winner in the creation of the Submission. No Submission or individual shall be deemed a winning Submission or winner until their post-competition prize affidavits have been completed and verified, even if prospective winners have been announced verbally or on the competition website. The final decision to designate a winner shall be made by the Sponsor and/or Administrator. A Submission can win a maximum of one prize. In the event that no entries are received for a region, no prize will be awarded.

On or about **December 9, 2025**, the potential winner(s) will be selected and may be notified by email, at Sponsor’s discretion for Winner Verification Requirement (as defined below). If a potential winner does not respond to the notification attempt within two days from the first notification attempt, then such potential winner will be disqualified and an alternate potential winner will be selected from among all eligible entries received based on the judging criteria described herein. Except where prohibited by law, each potential winner may be required to sign and return a Declaration of Eligibility and Liability and Publicity Release and provide any additional information that may be required by Sponsor. If required, potential winners must return all such required documents within two days following attempted notification or such potential winner will be deemed to have forfeited the prize and another potential winner will be selected based on the judging criteria described herein. All notification requirements, as well as other requirements within these Rules, will be strictly enforced.

The public Winner Announcement will be on or around **December 12, 2025**.

“Winner Verification Requirement” means THE AWARD OF A PRIZE TO A POTENTIAL WINNER IS SUBJECT TO VERIFICATION OF THE IDENTITY, QUALIFICATIONS AND ROLE OF THE POTENTIAL WINNER IN THE CREATION OF THE SUBMISSION. No Submission or individual shall be deemed a winning Submission or winner until their post-competition prize affidavits have been completed and verified, even if prospective winners have been announced verbally or on the competition website. The final decision to designate a winner shall be made by the Sponsor and/or Administrator.

Determinations of judges are final and binding.

**9. PRIZES:**

**A. PRIZES FOR EACH CATEGORY**

Winner Prize Quantity Eligible
AI Studio Category•$8,000 in USD

• $1,000 in Google Cloud Credits for use with a Cloud Billing Account (must be a single billing account)

• Virtual Coffee with a Google Team Member

• Social Promo 1 All eligible submissions that build there apps with AI Studio
AI Agents Category• $8,000 in USD

• $1,000 in Google Cloud Credits for use with a Cloud Billing Account

• Virtual Coffee with a Google Team Member

• Social Promo 1 All eligible submissions that implement AI Agents
GPU Category• $8,000 in USD

• $1,000 in Google Cloud Credits for use with a Cloud Billing Account (must be a single billing account)

• Virtual Coffee with a Google Team Member

• Social Promo 1 All eligible submissions that utilize GPUs

**B. PRIZES FOR GRAND PRIZE WINNER**

Winner Prize Quantity Eligible
Grand Prize• $20,000 in USD

• $3,000 in Google Cloud Credits for use with a Cloud Billing Account (must be a single billing account)

• 1 year of Google Developer Program Premium subscription at no-cost (up to two subscriptions)

• Virtual Coffee with a Google Team Member

• Social Promo 1 Top scoring Project across all categories
Honorable Mentions• $2,000 in USD

• $500 in Google Cloud Credits for use with a Cloud Billing Account ((must be a single billing account)3 Runners up from all eligible submissions

**C. Terms Applicable to All Prizes.**

**Cash Prize Delivery**: Cash Prizes will be payable to the winner, if an individual; to the winning team’s Representative, if a team; or to the organization, if the winning team is an Organization. It will be the responsibility of the winning team’s or organization’s Representative to allocate the Prize among their team or organization’s participating members, as the Representative deems appropriate. A monetary Prize will be mailed to the winner’s address (if an individual) or the Representative’s address (if a team or organization), or sent electronically to the winner, winning teams Representative, or organization’s bank account, only after receipt of the completed winner affidavit and other required forms (collectively the “Required Forms”), if applicable. The deadline for returning the Required Forms to the Administrator is ten (10) business days after the Required Forms are sent. Failure to provide correct information on the Required Forms, or other correct information required for the delivery of a Prize, may result in delayed Prize delivery, disqualification of the individual, team or organization or forfeiture of a Prize. Prizes will be delivered within sixty (60) days of the Sponsor or Devpost’s receipt of the completed Required Forms.

None of the non-cash prizes are redeemable for cash. The approximate retail value (ARV) may be adjusted depending on the country, state or jurisdiction of residence of the winner. All travel arrangements will be made by the traveler (or another party on traveler’s behalf) in its sole discretion. Travelers may be required to provide proof of travel, relevant receipts and sign and return additional Prize-related documents as are provided by Sponsor, or provide additional information as requested by Sponsor, including without limitation for purposes of receiving the reimbursement for the Travel Prize reimbursement.

Odds of winning any prize depends on the number of eligible entries received during the Contest Period and the skill of the entrants. No transfer, substitution or cash equivalent for prize(s) is allowed, except at Sponsor’s sole discretion. Sponsor reserves the right to substitute a prize, in whole or in part, of equal or greater monetary value if a prize cannot be awarded, in whole or in part, as described for any reason. Value is subject to market conditions, which can fluctuate and any difference between actual market value and ARV will not be awarded. The prize(s) may be subject to restrictions and/or licenses and may require additional hardware, software, service, or maintenance to use. The winner shall bear all responsibility for use of the prize(s) in compliance with any conditions imposed by such manufacturer(s), and any additional costs associated with its use, service, or maintenance. Contest Entities have not made and Contest Entities are not responsible in any manner for any warranties, representations, or guarantees, express or implied, in fact or law, relating to the prize(s), regarding the use, value or enjoyment of the prize(s), including, without limitation, its quality, mechanical condition, merchantability, or fitness for a particular purpose, with the exception of any standard manufacturer's warranty that may apply to the prize(s) or any components thereto.

**10. FEES & TAXES:**

Winners (and in the case of team or organization, all participating members) are responsible for any fees associated with receiving or using a prize, including but not limited to, wiring fees or currency exchange fees. Winners (and in the case of team or organization, all participating members) are responsible for reporting and paying all applicable taxes in their jurisdiction of residence (federal, state/provincial/territorial and local). Winners may be required to provide certain information to facilitate receipt of the award, including completing and submitting any tax or other forms necessary for compliance with applicable withholding and reporting requirements. United States residents may be required to provide a completed form W-9 and residents of other countries may be required to provide a completed W-8BEN form. Winners are also responsible for complying with foreign exchange and banking regulations in their respective jurisdictions and reporting the receipt of the Prize to relevant government departments/agencies, if necessary. The Sponsor, Devpost, and/or Prize provider reserves the right to withhold a portion of the prize amount to comply with the tax laws of the United States or other Sponsor jurisdiction, or those of a winner’s jurisdiction.

**11. GENERAL CONDITIONS:**

All federal, state, provincial and local laws and regulations apply. Google reserves the right to disqualify any entrant from the Contest if, in Google’s sole discretion, it reasonably believes that the entrant has attempted to undermine the legitimate operation of the Contest by cheating, deception, or other unfair playing practices or annoys, abuses, threatens or harasses any other entrants, Google, or the Judges.

**12. INTELLECTUAL PROPERTY RIGHTS:**

To the extent your or your team or organization’s Submission makes use of generally commercially available software not owned by you or your team or organization that was used to generate the Submission, but that can be procured by Google without undue expense, you do not grant the license in the preceding sentence to that software.

As between Google and the entrant, all Submissions remain the intellectual property of the individuals or organizations that developed them. The entrant retains ownership of all intellectual and industrial property rights (including moral rights) in and to any project materials, or videos provided for the Contest. As a condition of entry, entrant grants Google, its subsidiaries, agents and partner companies, a perpetual, irrevocable, worldwide, royalty-free, and non-exclusive license to use, reproduce, adapt, modify, publish, distribute, publicly perform, create a derivative work from, and publicly display such Project(s) (1) for the purposes of allowing Google and its affiliates and the Judges to evaluate the Project for purposes of the Contest, and (2) in connection with advertising and promotion via communication to the public or other groups, including, but not limited to, the right to make screenshots, animations and video clips available for promotional purposes.

**13. PRIVACY:**

Participant acknowledges and agrees that Google may collect, store, share and otherwise use personally identifiable information provided during the registration process and the contest, including, but not limited to, name, mailing address, phone number, and email address. Google will use this information in accordance with its Privacy Policy [(http://www.google.com/policies/privacy/)](http://www.google.com/policies/privacy/), including for administering the contest and verifying Participant’s identity, postal address and telephone number in the event an entry qualifies for a prize.

Participant’s information may also be transferred to countries outside the country of Participant's residence, including the United States. Such other countries may not have privacy laws and regulations similar to those of the country of Participant's residence.

If a participant does not provide the mandatory data required at registration, Google reserves the right to disqualify the entry.

Participant has the right to request access, review, rectification or deletion of any personal data held by Google in connection with the Contest by writing to Google at this email address [cloudhackathons@google.com](mailto:cloudhackathons@google.com).

**14. PUBLICITY:**

By participating in the Hackathon, Entrant consents to the promotion and display of the Entrant’s Submission, and to the use of personal information about themselves for promotional purposes, by the Sponsor, Administrator, and third parties acting on their behalf. Such personal information includes, but is not limited to, your name, likeness, photograph, voice, opinions, comments and hometown and country of residence. It may be used in any existing or newly created media, worldwide without further payment or consideration or right of review, unless prohibited by law. Authorized use includes but is not limited to advertising and promotional purposes.

**15. WARRANTY, INDEMNITY AND RELEASE:**

Entrants warrant that their Submissions are their own original work and, as such, they are the sole and exclusive owner and rights holder of the submitted Submission and that they have the right to submit the Submission in the Contest and grant all required licenses, except that to the extent your or your team or organization’s Submission makes use of generally commercially available software not owned by you or your team or organization that was used to generate the Submission, but that can be procured by Google without undue expense, you do not grant the license in the preceding sentence to that software. Each entrant agrees not to submit any Submission that (1) infringes any third party proprietary rights, intellectual property rights, industrial property rights, personal or moral rights or any other rights, including without limitation, copyright, trademark, patent, trade secret, privacy, publicity or confidentiality obligations; or (2) otherwise violates the applicable state or federal law. Each entrant further represents and warrants that it has the necessary rights and licenses to use any and all data used in or for the Submission and otherwise as necessary for the terms hereunder.To the maximum extent permitted by law, each entrant indemnifies and agrees to keep indemnified Contest Entities at all times from and against any liability, claims, demands, losses, damages, costs and expenses resulting from any act, default or omission of the entrant and/or a breach of any warranty set forth herein. To the maximum extent permitted by law, each entrant agrees to defend, indemnify and hold harmless the Contest Entities from and against any and all claims, actions, suits or proceedings, as well as any and all losses, liabilities, damages, costs and expenses (including reasonable attorneys fees) arising out of or accruing from (a) any Submission or other material uploaded or otherwise provided by the entrant that infringes any copyright, trademark, trade secret, trade dress, patent or other intellectual property right of any person or defames any person or modifies their rights of publicity or privacy, (b) any misrepresentation made by the entrant in connection with the Contest; (c) any non-compliance by the entrant with these Rules; (d) claims brought by persons or entities other than the parties to these Rules arising from or related to the entrant’s involvement with the Contest; and (e) acceptance, possession, misuse or use of any prize or participation in any Contest-related activity or participation in this Contest.

Entrant releases Google from any liability associated with: (a) any malfunction or other problem with the Contest Site; (b) any error in the collection, processing, or retention of entry information; or (c) any typographical or other error in the printing, offering or announcement of any prize or winners.

**16. ELIMINATION:**

Any false information provided within the context of the Contest by any entrant concerning identity, mailing address, telephone number, email address, ownership of right or non-compliance with these Rules or the like may result in the immediate elimination of the entrant from the Contest.

**17. INTERNET:**

Contest Entities are not responsible for any malfunction of the entire Contest Site or any late, lost, damaged, misdirected, incomplete, illegible, undeliverable, or destroyed Submissions or entry materials due to system errors, failed, incomplete or garbled computer or other telecommunication transmission malfunctions, hardware or software failures of any kind, lost or unavailable network connections, typographical or system/human errors and failures, technical malfunction(s) of any telephone network or lines, cable connections, satellite transmissions, servers or providers, or computer equipment, traffic congestion on the Internet or at the Contest Site, or any combination thereof, including other telecommunication, cable, digital or satellite malfunctions which may limit an entrant’s ability to participate.

**18. RIGHT TO CANCEL, MODIFY OR DISQUALIFY:**

If for any reason the Contest is not capable of running as planned, including infection by computer virus, bugs, tampering, unauthorized intervention, fraud, technical failures, or any other causes which corrupt or affect the administration, security, fairness, integrity, or proper conduct of the Contest, Google reserves the right at its sole discretion to cancel, terminate, modify or suspend the Contest. Google further reserves the right to disqualify any entrant who tampers with the submission process or any other part of the Contest or Contest Site. Any attempt by an entrant to deliberately damage any web site, including the Contest Site, or undermine the legitimate operation of the Contest is a violation of criminal and civil laws and should such an attempt be made, Google reserves the right to seek damages from any such entrant to the fullest extent of the applicable law.

**19. NOT AN OFFER OR CONTRACT OF EMPLOYMENT:**

Under no circumstances shall the submission of a Submission into the Contest, the awarding of a prize, or anything in these Rules be construed as an offer or contract of employment with either Google, or the Contest Entities. You acknowledge that you have submitted your Submission voluntarily and not in confidence or in trust. You acknowledge that no confidential, fiduciary, agency or other relationship or implied-in-fact contract now exists between you and Google or the Contest Entities and that no such relationship is established by your submission of a Submission under these Rules.

**20. FORUM AND RECOURSE TO JUDICIAL PROCEDURES:**

These Rules shall be governed by, subject to, and construed in accordance with the laws of the State of California, United States of America, excluding all conflict of law rules. If any provision(s) of these Rules are held to be invalid or unenforceable, all remaining provisions hereof will remain in full force and effect. To the extent permitted by law, the rights to litigate, seek injunctive relief or make any other recourse to judicial or any other procedure in case of disputes or claims resulting from or in connection with this Contest are hereby excluded, and all Participants expressly waive any and all such rights.

**21. ARBITRATION:**

By entering the Contest, you agree that exclusive jurisdiction for any dispute, claim, or demand related in any way to the Contest will be decided by binding arbitration. All disputes between you and Google of whatsoever kind or nature arising out of these Rules, shall be submitted to Judicial Arbitration and Mediation Services, Inc. (“JAMS”) for binding arbitration under its rules then in effect in the San Jose, California, USA area, before one arbitrator to be mutually agreed upon by both parties. The parties agree to share equally in the arbitration costs incurred.

**22. ADDITIONAL TERMS:**

Please review the Devpost Terms of Service at [https://info.devpost.com/terms](https://info.devpost.com/terms) for additional rules that apply to your participation in the Contest and more generally your use of the Contest Site. Such Terms of Service are incorporated by reference into these Official Rules, including that the term "Poster" in the Terms of Service shall mean the same as "Sponsor" in these Official Rules." If there is a conflict between the Terms of Service and these Official Rules, these Official Rules shall control with respect to this Contest only.

**23. ENTRANT'S PERSONAL INFORMATION:**

Information collected from entrants is subject to Devpost’s Privacy Policy, which is available at [https://info.devpost.com/privacy](https://info.devpost.com/privacy).

For questions, send an email to support@devpost.com.