const adminLogin = (name: string, password: string) => {
  cy.session(["superuser", name, password], () => {
    cy.visit("/admin/");
    cy.get('[name=username]').type(name)
    cy.get('[name=password]').type(password)
    cy.get('[type=submit]').click()
    cy.url().should('contain', '/admin/')
  })
  cy.visit("/admin/");
}

const regularLogin = (name: string, password: string) => {
  cy.session([name, password], () => {
    cy.visit("/");
    cy.get("[name=login]").type(name);
    cy.get("[name=password]").type(password);
    cy.get("[type=submit]").click();
  });
  cy.visit("/");
};

describe("Can Login To Admin Site", () => {
  beforeEach(() => {
    adminLogin("parrotmac@gmail.com", "test");
  });

  it("should be able to login as admin", () => {
    cy.visit("/admin/");
    cy.get("h1").contains("Site administration");
  });
});

describe("Can login to regular site", () => {
  beforeEach(() => {
    regularLogin("parrotmac@gmail.com", "test");
  });

  it("should be able to login and create a new list wishlist", () => {
    cy.url().should("contain", "/groups");
    cy.get('a').contains('New Group').click();
    cy.url().should('contain', '/groups/create');
    cy.get('[name=name]').clear().type('Test Group');
    cy.get('[type=submit]').click();
    cy.url().should('contain', '/groups');
    cy.get('a').contains('Create List').click();
    cy.url().should('contain', '/wishlists/create');
    cy.get('[name=title]').clear().type('Test List');
    cy.get('[type=submit]').click();
    cy.url().should('contain', '/wishlists/');
    cy.get('div.wishlist-page-header').find('a').contains('Add Item').click();
    cy.url().should('contain', '/items/create');
    cy.get('[name=title]').type('A Pony');
    cy.get('[name=description]').type('A pony would be nice');
    cy.get('ul.links').find('input').first().type('https://www.youtube.com/watch?v=QH2-TGUlwu4');
    cy.get('ul.links').find('button').click();
    cy.get('ul.links').find('input').eq(1).type('https://www.youtube.com/watch?v=QH2-TGUlwu4');
    cy.get('[type=submit]').click();
    cy.url().should('contain', '/wishlists/');
  });
});
