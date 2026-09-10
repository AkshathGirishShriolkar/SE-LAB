# Use-Case Flow Specification — Evaluate Feature Flag

**Use Case ID:** UC-001  
**Use Case Name:** Evaluate Feature Flag  
**Primary Actors:** Software Engineer, Release Manager  
**Goal:** Determine whether a feature flag is enabled for a particular user in a particular environment.

## Preconditions
1. The feature flag exists in the system.
2. The relevant targeting rules have been configured.
3. The user's identifying information is available.
4. The requested environment is configured.

## Postconditions
1. The system returns the evaluated boolean state of the feature flag.
2. The returned state reflects the applicable targeting rules and environment configuration.
3. No unauthorized modification to the feature-flag configuration occurs.

## Main Success Scenario
1. The actor/client requests the state of a feature flag for a particular user.
2. The system identifies the requested feature flag.
3. The system identifies the requested deployment environment.
4. The system retrieves the applicable targeting rules.
5. The system evaluates the user's attributes against the targeting rules.
6. The system determines whether the user belongs to the configured rollout/cohort.
7. The system applies any applicable environment override.
8. The system determines the final boolean feature-flag state.
9. The system returns the feature-flag state to the requesting client.

## Alternate Flow — User Does Not Match Targeting Rule
1. Steps 1–5 of the Main Success Scenario are performed.
2. The system evaluates the user's attributes against the configured targeting rules.
3. The user does not satisfy the targeting conditions.
4. The system determines that the feature flag should not be enabled for that user.
5. The system returns `false` as the feature-flag state.
6. The client continues using the existing/default feature behavior.

## Acceptance Criteria
**Pass:** A user belonging to the configured target cohort receives the correct feature-flag state.

**Fail:** A user outside the configured cohort incorrectly receives the enabled state.
