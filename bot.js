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
            await turnContext.sendActivity(`Searching`);
            var mongoClient = require('mongodb').MongoClient;
            var imageBase64Sting = "";
            if (turnContext.activity.attachments && turnContext.activity.attachments.length > 0) {
                console.log('There is an attachment');
                if (turnContext.activity.attachments[0].contentType === 'image/jpeg' || turnContext.activity.attachments[0].contentType === 'image/png') {
                    console.log('Attachment is jpg/png', turnContext.activity.attachments[0].contentUrl);
                    // Message with attachment, proceed to download it.
                    // Skype & MS Teams attachment URLs are secured bya JwtToken, so we need to pass the token from our bot.
                    var attachment = turnContext.activity.attachments[0];
                    var request = require('request-promise').defaults({ encoding: null });
                    var fileDownload = request(attachment.contentUrl);
                    var prom = await fileDownload.then(
                        function(response) {
                            // convert image to base64 string
                            imageBase64Sting = new Buffer(response, 'binary').toString('base64');
                        }).catch(function(err) {
                        console.log('Error downloading attachment:', { statusCode: err.statusCode, message: err.response.statusMessage });
                    });
                }
            }
            try {
                var client = await mongoClient.connect('mongodb://touchecosmos:ai8DvhOqzvpDsk0otnjmO6475SCIDzfzrykNqy5Jie5BtujcDcZCtUfontWqkCTmksCT7521s3as0OUlYLCghQ%3D%3D@touchecosmos.documents.azure.com:10255/?ssl=true');
                var db = client.db('testdb');

                // var dateTime = new Date();
                // console.log('Date Time ', dateTime);
                console.log('Input ', turnContext.activity.text);
                console.log('Timestamp', turnContext.activity.timestamp.toString());
                var result = await db.collection('Testcoll').insertOne({
                    'timestamp': turnContext.activity.timestamp.toString(),
                    'input': turnContext.activity.text,
                    'attachment': imageBase64Sting
                });
                var spawn = require('child_process');
                var pyProg = spawn.spawnSync('python', ['_test.py', result.insertedId]);
                console.log('Immediate output is ', pyProg.stdout.toString());
                console.log('Inserted a document into the testdb collection.', result.insertedId);
                var id = require('mongodb').ObjectID(result.insertedId);
                var output = await db.collection('Testcoll').findOne({'_id':id}, {input: 1});
                console.log('Printing output output', output.output);
                await client.close();
            } catch (err) {
                console.log(err.stack);
            }
            console.log('Status ', pyProg.status.toString());
            console.log('Error ', pyProg.stderr.toString());
            await turnContext.sendActivity(`${ output.output }`);
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