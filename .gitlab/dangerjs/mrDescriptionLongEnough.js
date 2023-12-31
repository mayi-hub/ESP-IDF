const { recordRuleExitStatus } = require("./configParameters.js");

/**
 * Check if MR Description has accurate description".
 *
 * @dangerjs WARN
 */
module.exports = function () {
    const ruleName = "Merge request sufficient description";
    const mrDescription = danger.gitlab.mr.description;
    const descriptionChunk = mrDescription.match(/^([^#]*)/)[1].trim(); // Extract all text before the first section header (i.e., the text before the "## Release notes")

    const shortMrDescriptionThreshold = 50; // Description is considered too short below this number of characters

    if (descriptionChunk.length < shortMrDescriptionThreshold) {
        recordRuleExitStatus(ruleName, "Failed");
        return warn(
            "The MR description looks very brief, please check if more details can be added."
        );
    }

    // At this point, the rule has passed
    recordRuleExitStatus(ruleName, "Passed");
};
