const modifiedStates = ["hard", "good"];
let lastStateStep = 0;
for (const [j, state] of Object.entries(modifiedStates)) {
    const relearning = states[state].normal?.relearning;
    if (relearning && relearning.remainingSteps !== 1) {
        let i = 0;
        for (
            i = lastStateStep;
            i < globalThis.relearningSteps.length - 1 &&
            globalThis.relearningSteps[i] < globalThis.lastReviewTime;
            i++
        );
        if (i !== globalThis.relearningSteps.length - 1) i++;
        i -= modifiedStates.length - j - 1;
        relearning.remainingSteps = globalThis.relearningSteps.length - i;
        relearning.scheduledSecs = globalThis.relearningSteps[i];
        lastStateStep = i + 1 !== globalThis.relearningSteps.length ? i + 1 : i;
    }
}
