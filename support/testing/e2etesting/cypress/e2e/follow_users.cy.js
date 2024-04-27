const endpoint = '/'
describe('search a user', () => {
    beforeEach(() => {
        cy.loginByUI('user1', 'user');
      });

    it('searches for a user', () => {
        cy.visit(endpoint)

        cy.contains('Hello, user1')
        // todo needs implementation once following fixes
        // search user by username 'user2 input with placeholder: Search by username
        // cy.get('input[placeholder="Search by username"]').type('user2')
        // // click on search button
        // cy.get('button').contains("Search").click()

        // // assert that button with text 'user2' is visible
        // cy.get('button').contains("user2").should('be.visible')

        // // click on button with text 'user2'
        // cy.get('button').contains("user2").click()
        // //wait for url to change
        // cy.url().should('include', '/profile') 
    })


    // it('can follow a user', () => {
    //     cy.visit(endpoint)
    //     // search user by username 'user2 input with placeholder: Search by username
    //     cy.get('input[placeholder="Search by username"]').type('user2')
    //     // click on search button
    //     cy.get('button').contains("Search").click()


    //     // click on button with text 'user2'
    //     cy.get('button').contains("user2").should('be.visible').click()
    //     cy.url().should('include', '/profile') 

    //     // click on follow button
    //     cy.get('button').contains("Follow").click()
    // })


    // // register as a seeded user
    // it('lets one login', () => {
    //   cy.visit(endpoint)
    //   cy.contains('Sign In').click()
    //   cy.url().should('include', '/sign-in')
  
    //   cy.get('input[id="profile-name"]').type(userName)
    //   cy.get('input[id="password"]').type(userPassword)
  
    //   cy.get('button').contains("Sign In").click()
  
    //   // redirect to / -> sometimes we get redirected to /onboarding, redirect back manually
  
    //   cy.url().should('not.eq', endpoint+'/') // kinda a workload ->wait for redirect doesn't matter to what
  
    //   cy.visit(endpoint)
    //   cy.contains('Hello, '+userName)
    //   // now we open preferences, because the user was seeded
    // })
  })