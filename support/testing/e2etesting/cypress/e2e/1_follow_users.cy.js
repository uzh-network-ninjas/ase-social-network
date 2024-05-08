const endpoint = Cypress.config('baseUrl')

const secondUser = 'user2'
describe('search a user', () => {
  beforeEach(() => {
      cy.loginByUI('user1', 'user');
    });

  it('searches for a user', () => {
      cy.visit(endpoint+'/home')

      cy.contains('Home')
      // get button with "Search User"
      cy.contains("Search User").click()
      // wait for uer to be /search-user
      cy.url().should('include', '/search-user')
      // search user by username 'user2 input with id "search_user_field"
      cy.get('input[id="search_user_field"]').type(secondUser) 

      // press enter
      cy.get('input[id="search_user_field"]').type('{enter}')

      // assert that div with text 'user2' is visible
      cy.get('div').contains(secondUser).should('be.visible')

      // click on button with text 'user2'
      cy.get('div').contains(secondUser).click()
      //wait for url to change
      cy.url().should('include', '/profile') 
  })

  it('can follow user', () => {
    cy.visit(endpoint+'/search-user')

    cy.get('input[id="search_user_field"]').type(secondUser) 
    cy.get('input[id="search_user_field"]').type('{enter}')

    // assert that div with text 'user2' is visible
    cy.get('div').contains(secondUser).should('be.visible')

    // click on button with text 'user2'
    cy.get('div').contains(secondUser).click()
    //wait for url to change
    cy.url().should('include', '/profile') 

    cy.contains('div', 'Followers').parent().find('div.text-2xl').then($div => {
      const initialFollowers = parseInt($div.text() || 0);
      
      // Click on follow button
      cy.get('button').contains("Follow").click();
  
      // Verify that followers count is initialFollowers + 1
      cy.contains('div', 'Followers').parent().find('div.text-2xl').should($div => {
        const newFollowers = parseInt($div.text());
        expect(newFollowers).to.eq(initialFollowers + 1);
      });
    });

  })

  // it("after following user2 I follow him as well", () =>{
  //   cy.visit(endpoint+"/home");
  //   cy.wait(3000);

  //   // Click the button to open the overlay menu
  //   // This uses attributes to uniquely identify the button
  //   cy.get('button[aria-haspopup="true"][data-pc-name="button"]').click();

  //   // Ensure the overlay menu is visible before attempting to interact with it
  //   cy.get('#overlay_menu').should('be.visible');

  //   // Click on the 'Profile' link within the overlay menu
  //   // Uses role and text to identify the link accurately
  //   cy.get('#overlay_menu').find('a').contains('Profile').click();

  //   // Optionally verify the URL or page content to confirm navigation to the profile
  //   cy.url().should('include', '/profile');

  //   // add delay -> wait for load (we need to load all review)
  //   cy.wait(3000);

  //   cy.contains('div', 'Follows').parent().find('div.text-2xl').then($div => {
  //     const nr_follows = parseInt($div.text());
  //     // should be 1
  //     expect(nr_follows).to.eq(1);
  //   });

  // })
})