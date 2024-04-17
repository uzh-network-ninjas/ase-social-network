// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
Cypress.Commands.add('loginByUI', (username, password) => {

    cy.visit('/sign-in')
    cy.get('input[id="profile-name"]').type(username)
    cy.get('input[id="password"]').type(password)
    cy.get('button').contains("Sign In").click()
    cy.url().should('not.eq', Cypress.config('baseUrl')+'/sign-in') // kinda a workload ->wait for redirect doesn't matter to what
  });