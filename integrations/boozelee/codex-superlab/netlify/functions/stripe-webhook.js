const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const nodemailer = require('nodemailer');

exports.handler = async (event) => {
  const sig = event.headers['stripe-signature'];
  let stripeEvent;
  try {
    stripeEvent = stripe.webhooks.constructEvent(event.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return { statusCode: 400, body: `Webhook Error: ${err.message}` };
  }
  if (stripeEvent.type === 'checkout.session.completed') {
    const email = stripeEvent.data.object.customer_email;
    let transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.SUPPORT_EMAIL,
        pass: process.env.SMTP_PASSWORD
      }
    });
    await transporter.sendMail({
      from: process.env.SUPPORT_EMAIL,
      to: email,
      subject: 'Welcome to Codex SuperLab!',
      html: `
        <h2>🎉 Welcome to Codex SuperLab!</h2>
        <p>Thanks for your purchase!</p>
        <p><strong>Your access:</strong></p>
        <ul>
          <li><a href="https://github.com/BoozeLee/codex-superlab">GitHub Repository</a></li>
          <li><a href="${process.env.DISCORD_INVITE_LINK}">Discord Community</a></li>
        </ul>
      `
    });
  }
  return { statusCode: 200, body: 'Success' };
};
