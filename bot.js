// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

// bot.js is your bot's main entry point to handle incoming activities.

const { ActivityTypes } = require('botbuilder');

// Turn counter property
const TURN_COUNTER_PROPERTY = 'turnCounterProperty';

class EchoBot {
    /**
     *
     * @param {ConversationState} conversation state object
     */
    constructor(conversationState) {
        // Creates a new state accessor property.
        // See https://aka.ms/about-bot-state-accessors to learn more about the bot state and state accessors
        this.countProperty = conversationState.createProperty(TURN_COUNTER_PROPERTY);
        this.conversationState = conversationState;
    }
    /**
     *
     * Use onTurn to handle an incoming activity, received from a user, process it, and reply as needed
     *
     * @param {TurnContext} on turn context object.
     */
    async onTurn(turnContext) {
        // Handle message activity type. User's responses via text or speech or card interactions flow back to the bot as Message activity.
        // Message activities may contain text, speech, interactive cards, and binary or unknown attachments.
        // see https://aka.ms/about-bot-activity-message to learn more about the message and other activity types
        if (turnContext.activity.type === ActivityTypes.Message) {
            // read from state.
            let count = await this.countProperty.get(turnContext);
            count = count === undefined ? 1 : ++count;
            await turnContext.sendActivity(`Checking for spam "${ turnContext.activity.text }"`);
            var mongoClient = require('mongodb').MongoClient;
            var input = turnContext.activity.text;
            var timestamp = turnContext.activity.timestamp;
            try {
                var client = await mongoClient.connect('mongodb://touchecosmos:ai8DvhOqzvpDsk0otnjmO6475SCIDzfzrykNqy5Jie5BtujcDcZCtUfontWqkCTmksCT7521s3as0OUlYLCghQ%3D%3D@touchecosmos.documents.azure.com:10255/?ssl=true');
                var db = client.db('testdb');

                // var dateTime = new Date();
                // console.log('Date Time ', dateTime);
                console.log('Input ', input);
                console.log('Timestamp', timestamp);
                var result = await db.collection('Testcoll').insertOne({
                    'timestamp': timestamp,
                    'input': input
                });
                var spawn = require('child_process');
                var pyProg = spawn.spawnSync('python', ['test.py', result.insertedId]);
                console.log('DataString outside is ', pyProg.stdout.toString());
                console.log('Inserted a document into the testdb collection.', result.insertedId);

                await client.close();
            } catch (err) {
                console.log(err.stack);
            }
            // console.log('DataString outside is ', pyProg.status.toString());
             console.log('DataString outside is ', pyProg.stderr.toString());
            // await turnContext.sendActivity(`${ pyProg.stdout.toString() }`);
            await turnContext.sendActivity(`Checked for spam1 "${ turnContext.activity.text }"`);
            // increment and set turn counter.
            await this.countProperty.set(turnContext, count);
        } else {
            // Generic handler for all other activity types.
            await turnContext.sendActivity(`[${ turnContext.activity.type } event detected]`);
        }
        // Save state changes
        await this.conversationState.saveChanges(turnContext);
    }
}

exports.EchoBot = EchoBot;